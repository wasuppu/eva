# Default AST node factories
class DefaultFactory:
    def Program(self, body):
        return {'type': 'Program', 'body': body}

    def EmptyStatement(self):
        return {'type': 'EmptyStatement'}

    def BlockStatement(self, body):
        return {'type': 'BlockStatement', 'body': body}

    def ExpressionStatement(self, expression):
        return {'type': 'ExpressionStatement', 'expression': expression}

    def StringLiteral(self, value):
        return {'type': 'StringLiteral', 'value': value}

    def NumbericLiteral(value):
        return {'type': 'NumericLiteral', 'value': value}

# S-expression AST node factories
class SexpFactory:
    def Program(self, body):
        return ['begin', body]

    def EmptyStatement(self):
        return

    def BlockStatement(self, body):
        return ['begin', body]

    def ExpressionStatement(self, expression):
        return expression

    def StringLiteral(self, value):
        return f'"{value}"'

    def NumbericLiteral(self, value):
        return value

AST_MODE = 'sexp'
if AST_MODE == 'default':
    factory = DefaultFactory()
else:
    factory = SexpFactory()

