import json
import os
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
        dir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(dir, filename)
        with open(fpath, 'w') as file:
            file.write(code)

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

        # Blocks.
        if exp[0] == 'begin':
            _tag, *expressions = exp

            body = []
            for expression in expressions:
                body.append(self._toStatement(self.gen(expression)))
            return {'type': 'BlockStatement', 'body': body}

        raise Exception('Unexpected expression ' + json.dumps(exp))

    # Converts an expression to a statement.
    def _toStatement(self, exp):
        if exp['type'] == 'NumericLiteral' or exp['type'] == 'StringLiteral':
            return {'type': 'ExpressionStatement', 'expression': exp}
        else:
            return exp

# Whether expression is a number.
def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

# Whether expression is a string.
def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')