import json
from JSCodegen import JSCodegen

# JSCodegen instance
jsCodegen = JSCodegen()

# Eva MPP to JavaScript transpiler.
class EvaMPP:
    # Compiles Eva MPP program to JavaScript.
    def compile(self, program):
        # 1. Parse source code:
        evaAST = program
        # 2. Translate to JavaScript AST:
        jsAST = self.gen(evaAST)
        # 3. Generate JavaScript code:
        target = jsCodegen.generate(jsAST)
        # 4. Write compiled code to file:
        # self.saveToFile('./out.js', target)

        return {'ast': jsAST, 'target': target}

    # Saves compiled code to file.
    def saveToFile(self, filename, code):
        pass

    # Transpiles Eva AST to JavaScript AST.
    def gen(self, exp):
        # Self-evaluating expressions.
        if isNumber(exp):
            return {'type': 'NumericLiteral', 'value': exp}
        raise Exception('Unexpected expression ' + json.dumps(exp))

def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)