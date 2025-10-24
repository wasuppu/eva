# Letter parser: recursive descent implementation.
class Parser:
    # Parsers a string into an AST.
    def parse(self, string):
        self._string = string

        # Parse recursively starting from the main entry point,
        # the Program:
        return self.program()

    '''
    Main entry point.

    Program
        : NumericLiteral
        ;
    '''
    def program(self):
        return self.NumbericLiteral()

    '''
    NumericLiteral
        : NUMBER
        ;
    '''
    def NumbericLiteral(self):
        return {'type': 'NumericLiteral', 'value':toNumber(self._string)}

def toNumber(s):
    try:
        return int(s)
    except ValueError:
        return float(s)