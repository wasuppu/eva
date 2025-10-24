# JavaScript code generator.
class JSCodegen:
    # Generates code for Program.
    def generate(self, exp):
        return self.gen(exp)

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
        return exp['value']