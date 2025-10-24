import json
import os
import re
from JSCodegen import JSCodegen
from sexp import Sexp

evaParser = Sexp()
# JSCodegen instance
jsCodegen = JSCodegen()

# Eva MPP to JavaScript transpiler.
class EvaMPP:
    # Compiles Eva MPP program to JavaScript.
    def compile(self, program):
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
const {{print}} = require('./runtime');

{code}
        '''
        dir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(dir, filename)
        with open(fpath, 'w') as file:
            file.write(out)

    # Codegen entire program.
    def genProgram(self, programBlock):
        _tag, *expressions = programBlock

        body = []
        for expression in expressions:
            body.append(self._toStatement(self.gen(expression)))

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

            body = []
            for expression in expressions:
                body.append(self._toStatement(self.gen(expression)))
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

        # Function calls.
        if isinstance(exp, list):
            fnName = self._toVariableName(exp[0])
            callee = self.gen(fnName)
            return {
                'type': 'CallExpression',
                'callee': callee,
                'arguments': list(map(lambda arg: self.gen(arg), exp[1:]))
            }

        raise Exception('Unexpected expression ' + json.dumps(exp))

    # Converts an expression to a statement.
    def _toStatement(self, exp):
        if (exp['type'] == 'NumericLiteral' or
            exp['type'] == 'StringLiteral' or
            exp['type'] == 'AssignmentExpression' or
            exp['type'] == 'Identifier' or
            exp['type'] == 'CallExpression'):
            return {'type': 'ExpressionStatement', 'expression': exp}
        else:
            return exp

    # Converts an Eva variable name to JS format.
    def _toVariableName(self, exp):
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