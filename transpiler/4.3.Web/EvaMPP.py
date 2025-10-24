import json
import os
import re
from JSCodegen import JSCodegen
from JSTransform import JSTransform

from sexp import Sexp

evaParser = Sexp()
# JSCodegen instance
jsCodegen = JSCodegen()
# JSTransform instance
jsTransform = JSTransform()

# Eva MPP to JavaScript transpiler.
class EvaMPP:
    # Compiles Eva MPP program to JavaScript.
    def compile(self, program):
        # Functions map.
        self._functions = {}
        self._currentBlock = []
        self._currentFn = None
        # 1. Parse source code:
        evaAST = evaParser.parse(f'(begin {program})')
        # 2. Translate to JavaScript AST:
        jsAST = self.genProgram(evaAST)
        # 3. Generate JavaScript code:
        target = jsCodegen.generate(jsAST)
        # 4. Write compiled code to file:
        self.saveToFile('./out.js', target)

        return {'ast': jsAST, 'target': target}

    # Saves compiled code to file.
    def saveToFile(self, filename, code):
        out = f'''// Prologue:
const {{print, spawn, sleep, scheduler, NextMatch, send, receive}} = require('./runtime');

{code}
        '''
        dir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(dir, filename)
        with open(fpath, 'w') as file:
            file.write(out)

    # Codegen entire program.
    def genProgram(self, programBlock):
        _tag, *expressions = programBlock

        prevBlock = self._currentBlock
        self._currentBlock = []
        body = self._currentBlock

        for expression in expressions:
            body.append(self._toStatement(self.gen(expression)))

        self._currentBlock = prevBlock

        return {'type': 'Program', 'body': body}

    # Transpiles Eva AST to JavaScript AST.
    def gen(self, exp):

        # Self-evaluating expressions.
        if isNumber(exp):
            return {'type': 'NumericLiteral', 'value': exp}

        if isString(exp):
            return {'type': 'StringLiteral', 'value': exp[1:-1]}

        if isVariableName(exp):
            return {'type': 'Identifier', 'name': self._toVariableName(exp)}

        # Blocks.
        if exp[0] == 'begin':
            _tag, *expressions = exp

            prevBlock = self._currentBlock
            self._currentBlock = []
            body = self._currentBlock

            for expression in expressions:
                body.append(self._toStatement(self.gen(expression)))

            self._currentBlock = prevBlock

            return {'type': 'BlockStatement', 'body': body}

        # Variables: (var x 10)
        if exp[0] == 'var':
            return {'type': 'VariableDeclaration', 'declarations': [
                {
                    'type': 'VariableDeclarator',
                    'id': self.gen(self._toVariableName(exp[1])),
                    'init': self.gen(exp[2]),
                }
            ]}

        # Variable update: (set x 10)
        if exp[0] == 'set':
            return {
                'type': 'AssignmentExpression',
                'operator': '=',
                'left': self.gen(self._toVariableName(exp[1])),
                'right': self.gen(exp[2])
            }

        # --: Syntactic sugar
        if exp[0] == '--':
            return {
                'type': 'BinaryExpression',
                'operator': '-',
                'left': self.gen(exp[1]),
                'right': self.gen(1),
            }

        # Unary expression.
        if isUnary(exp):
            operator = exp[0]

            if operator == 'not':
                operator = '!'
            return {'type': 'UnaryExpression', 'operator': operator, 'argument': self.gen(exp[1])}

        # Binary expression.
        if isBinary(exp):
            return {
                'type': 'BinaryExpression',
                'operator': exp[0],
                'left': self.gen(exp[1]),
                'right': self.gen(exp[2]),
            }

        # Logical binary expression.
        if isLogicalBinary(exp):
            operator = exp[0]

            if operator == 'or':
                operator = '||'
            elif operator == 'and':
                operator = '&&'
            else:
                raise Exception(f"Unknown logical operator {operator}")

            return {
                'type': 'LogicalExpression',
                'operator': operator,
                'left': self.gen(exp[1]),
                'right': self.gen(exp[2]),
            }

        # If statement: (if <test> <consequent> <alternate>)
        if exp[0] == 'if':
            return {
                'type': 'IfStatement',
                'test': self.gen(exp[1]),
                'consequent': self._toStatement(self.gen(exp[2])),
                'alternate': self._toStatement(self.gen(exp[3]))
            }

        # While loop
        if exp[0] == 'while':
            return {
                'type': 'WhileStatement',
                'test': self.gen(exp[1]),
                'body': self._toStatement(self.gen(exp[2])),
            }

        # For loop: Syntactic sugar
        if exp[0] == 'for':
            if len(exp) == 5:
              exp = ['begin', exp[1], ['while', exp[2], ['begin', exp[4], ['set', 'i', exp[3]]]]]
              return self.gen(exp)
            else:
                raise Exception('incorrect for expression ' + json.dumps(exp))

        # Functions.
        if exp[0] == 'def':
            id = self.gen(self._toVariableName(exp[1]))
            params = list(map(lambda e: self.gen(e), exp[2]))
            bodyExp = exp[3]

            if not hasBlock(bodyExp):
                bodyExp = ['begin', bodyExp]

            last = bodyExp[len(bodyExp) - 1]

            if not isStatement(last) and last[0] != 'return':
                bodyExp[len(bodyExp) - 1] = ['return', last]

            fn = {
                'type': 'FunctionDeclaration',
                'id': id,
                'params': params,
                'body': None
            }

            prevFn = self._currentFn
            self._currentFn = fn

            fn['body'] = self.gen(bodyExp)

            self._currentFn = prevFn

            self._functions[id['name']] = {
                'fn': fn,
                'definingBlock': self._currentBlock,
                'index': len(self._currentBlock)
            }

            return fn

        # Return: (return x)
        if exp[0] == 'return':
            return {
                'type': 'ReturnStatement',
                'argument': self.gen(exp[1])
            }

        # List: (list 1 2 3)
        if exp[0] == 'list':
            elements = list(map(lambda element: self.gen(element), exp[1:]))
            return {
                'type': 'ArrayExpression',
                'elements': elements,
            }

        # List index: (idx p 0)
        if exp[0] == 'idx':
            return {
                'type': 'MemberExpression',
                'computed': True,
                'object': self.gen(exp[1]),
                'property': self.gen(exp[2]),
            }

        # Record: (rec (key value) key)
        if exp[0] == 'rec':
            def genProperty(entry):
                key = value = None
                if isinstance(entry, list):
                    key = self.gen(entry[0])
                    value = self.gen(entry[1])
                else:
                    key = self.gen(entry)
                    value = key
                return {
                    'type': 'ObjectProperty',
                    'key': key,
                    'value': value
                }

            properties = list(map(genProperty, exp[1:]))
            return {
                'type': 'ObjectExpression',
                'properties': properties
            }

        # Property access: (prop p x)
        if exp[0] == 'prop':
            return {
                'type': 'MemberExpression',
                'object': self.gen(exp[1]),
                'property': self.gen(exp[2]),
            }

        # Pattern matching: (match value pattern1 handler1 ...)
        if exp[0] == 'match':
            value = self.gen(exp[1])

            topLevelTry = None
            insertBlock = None
            i = 2

            while True:
                pattern, ifNode = jsTransform.expressionToMatchPattern(self.gen(exp[i]), value)

                handler = self._toStatement(self.gen(exp[i+1]))

                tryBody = [handler]
                if handler['type'] == 'BlockStatement':
                    tryBody = [*handler['body']]

                # Reached "always match" / default:
                if pattern == None and ifNode == None:
                    insertBlock['body'].append(handler)
                    return topLevelTry

                # Extra if-check for value match:
                if ifNode != None:
                    tryBody.insert(0, ifNode)

                # Extra destructuring for complex patterns:
                if pattern != None:
                    destructVar = {
                        'type': 'VariableDeclaration',
                        'declarations': [{
                            'type': 'VariableDeclarator',
                            'id': pattern,
                            'init': value,
                        }]
                    }

                    tryBody.insert(0, destructVar)

                # catch (e) { ... }
                catchParam = {
                    'type' : 'Identifier',
                    'name': 'e',
                }

                # if (e != NextMatc) throw e;
                nextMatchIf = {
                    'type': 'IfStatement',
                    'test': {
                        'type': 'BinaryExpression',
                        'operator': '!=',
                        'left': catchParam,
                        'right': {
                            'type': 'Identifier',
                            'name': 'NextMatch',
                        }
                    },
                    'consequent': {
                        'type': 'ThrowStatement',
                        'argument': catchParam,
                    }
                }

                tryNode = {
                    'type': 'TryStatement',
                    'block': {
                        'type': 'BlockStatement',
                        'body': tryBody,
                    },
                    'handler': {
                        'type': 'CatchClause',
                        'param': catchParam,
                        'body': {
                            'type': 'BlockStatement',
                            'body': [nextMatchIf],
                        }
                    }
                }

                if insertBlock != None:
                    insertBlock['body'].append(tryNode)

                if topLevelTry == None:
                    topLevelTry = tryNode

                # Next insert block:
                insertBlock = tryNode['handler']['body']

                i+=2
                if i >= len(exp):
                    break

            return topLevelTry

        # Receive pattern matching: (receive value pattern1 handler1 ...)
        # Syntactic sugar for awaiting a message and calling (match ...)
        if exp[0] == 'receive':
            # If receive is met, we should update the current function to an async generator:
            self._currentFn['id']['name'] = f"_{self._currentFn['id']['name']}"
            self._currentFn['async'] = True
            self._currentFn['generator'] = True

            awaitVar = {
                'type': 'VariableDeclaration',
                'declarations': [
                    {
                    'type': 'VariableDeclarator',
                    'id': self.gen(exp[1]),
                    'init': {
                        'type': 'AwaitExpression',
                        'argument': {
                            'type': 'CallExpression',
                            'callee': {
                                'type': 'Identifier',
                                'name': 'receive',
                            },
                            'arguments': [{'type': 'ThisExpression'}],
                        },
                    }
                }]
            }

            # Convert to (match ...)
            exp[0] = 'match'

            matchExp = self.gen(exp)

            return {
                'type': 'BlockStatement',
                'body': [awaitVar, matchExp],
            }

        # Function calls.
        if isinstance(exp, list):
            fnName = self._toVariableName(exp[0])

            isRecursiveGenCall = (self._currentFn != None
                and self._currentFn.get('generator')
                and self._currentFn['id']['name'][1:] == fnName)

            if isRecursiveGenCall:
                fnName = self._currentFn['id']['name']

            callee = self.gen(fnName)
            args = list(map(lambda arg: self.gen(arg), exp[1:]))

            # Convert sleep(...) to await sleep(...)
            if callee['name'] == 'sleep':
                return {
                    'type': 'AwaitExpression',
                    'argument': {
                        'type': 'CallExpression',
                        'callee': callee,
                        'arguments': args
                    }
                }

            # Dynamically allocate a process function if the original function is used in the spawn(...) call:
            if callee['name'] == 'spawn':
                fnName = args[0]['name']
                processName = f"_{fnName}"
                if processName not in self._functions:
                    # Create a process handler from the original function.
                    processFn = jsTransform.functionToAsyncGenerator(self._functions[fnName]['fn'])

                    self._functions[processName] = self._functions[fnName].copy()
                    self._functions[processName].update({
                        'fn': processFn,
                        'index': self._functions[fnName]['index'] + 1,
                    })

                    # And push it to the same block where the original function is defined.
                    self._functions[fnName]['definingBlock'].insert(self._functions[processName]['index'], processFn)
                args[0]['name'] = processName

            # Recursive calls to process functions
            # are handled as delegate yield* expression.
            #
            # Note: we should call in the context of the current (this) process:
            #
            # foo (x, y) -> yield* foo.call(this, x, y)
            if isRecursiveGenCall:
                return {
                    'type': 'YieldExpression',
                    'delegate': True,
                    'argument': {
                        'type': 'CallExpression',
                        'callee': {
                            'type': 'MemberExpression',
                            'object': callee,
                            'property': {
                                'type': 'Identifier',
                                'name': 'call'
                            }
                        },
                        'arguments': [{'type': 'ThisExpression'}, *args]
                    }
                }

            return {
                'type': 'CallExpression',
                'callee': callee,
                'arguments': args,
            }

        raise Exception('Unexpected expression ' + json.dumps(exp))

    # Converts an expression to a statement.
    def _toStatement(self, exp):
        if (exp['type'] == 'NumericLiteral' or
            exp['type'] == 'StringLiteral' or
            exp['type'] == 'AssignmentExpression' or
            exp['type'] == 'Identifier' or
            exp['type'] == 'CallExpression' or
            exp['type'] == 'BinaryExpression' or
            exp['type'] == 'LogicalExpression' or
            exp['type'] == 'UnaryExpression' or
            exp['type'] == 'YieldExpression' or
            exp['type'] == 'ArrayExpression' or
            exp['type'] == 'MemberExpression' or
            exp['type'] == 'ThisExpression' or
            exp['type'] == 'AwaitExpression'
            ):
            return {'type': 'ExpressionStatement', 'expression': exp}
        else:
            return exp

    # Converts an Eva variable name to JS format.
    def _toVariableName(self, exp):
        if exp == 'self':
            return 'this'

        return self._toJSName(exp)

    # Converts dash-name (Eva) to camelCases (JS).
    def _toJSName(self, name):
        return re.sub(r'-([a-z])', lambda m: m.group(1).upper(), name)


# Whether expression is a number.
def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

# Whether expression is a string.
def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')

# Whether expression is a variable name.
def isVariableName(exp):
    return (type(exp) == str) and re.search(r"^[+\-*/<>=a-zA-Z0-9_\.]+$", exp)

# Whether the expression is a binary.
def isBinary(exp):
    if len(exp) != 3:
        return False
    return (exp[0] == '+' or
            exp[0] == '-' or
            exp[0] == '*' or
            exp[0] == '/' or
            exp[0] == '==' or
            exp[0] == '!=' or
            exp[0] == '>' or
            exp[0] == '<' or
            exp[0] == '>=' or
            exp[0] == '<=')

# Whether the expression is a logical.
def isLogicalBinary(exp):
    if len(exp) != 3:
        return False
    return exp[0] == 'or' or exp[0] == 'and'

# Whether the expression is unary.
def isUnary(exp):
    if len(exp) != 2:
        return False
    return exp[0] == 'not' or exp[0] == '-'

# Whether Eva code creates a block.
def hasBlock(exp):
    return exp[0] == 'begin' or exp[0] == 'receive'

# Whether Eva code is a statement.
def isStatement(exp):
    return (exp[0] == 'begin' or
            exp[0] == 'if' or
            exp[0] == 'while' or
            exp[0] == 'var')
