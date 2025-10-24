# JavaScript code generator.
class JSCodegen:
    # Codegen options.
    def __init__(self, indent = 2):
        self._indent = indent
        self._currentIndent = 0

    # Generates code for Program.
    def generate(self, exp):
        return self.Program(exp)

    # Program.
    def Program(self, exp):
        return '\n'.join(map(lambda e: self.gen(e), exp['body']))

    # Generates code for a JS node.
    def gen(self, exp):
        try:
            method = getattr(self, exp['type'])
            return method(exp)
        except AttributeError:
            print('Unexpected expression: ' + exp['type'])
            raise

    # NumericLiteral.
    def NumericLiteral(self, exp):
        return str(exp['value'])

    # StringLiteral.
    def StringLiteral(self, exp):
        # return '"%s"'%(exp['value'])
        return f'''"{exp['value']}"'''

    # Identifier.
    def Identifier(self, exp):
        return exp['name']

    # VariableDeclaration.
    def VariableDeclaration(self, exp):
        declarations = exp['declarations'][0]
        _type, id, init = declarations.values()
        return f"let {self.gen(id)} = {self.gen(init)};"

    # AssignmentExpression.
    def AssignmentExpression(self, exp):
        _type, operator, left, right = exp.values()
        return f"{self.gen(left)} {operator} {self.gen(right)}"

    # CallExpression
    def CallExpression(self, exp):
        callee = self.gen(exp['callee'])
        args = ', '.join(map(lambda arg: self.gen(arg), exp['arguments']))
        return f"{callee}({args})"

    # BlockStatement.
    def BlockStatement(self, exp):
        self._currentIndent += self._indent
        result = '{\n' + '\n'.join(map(lambda e: self._ind() + self.gen(e), exp['body'])) +'\n'
        self._currentIndent -= self._indent
        result += self._ind() + '}'
        return result

    # ExpressionStatement.
    def ExpressionStatement(self, exp):
        return self.gen(exp['expression']) + ';'

    # Indent print.
    def _ind(self):
        return ' ' * self._currentIndent