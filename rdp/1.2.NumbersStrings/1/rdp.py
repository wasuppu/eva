from tokenizer import Tokenizer

# Letter parser: recursive descent implementation.
class Parser:
    # Initializes the parser.
    def __init__(self):
        self._string = ''
        self._tokenizer = None

    # Parsers a string into an AST.
    def parse(self, string):
        self._string = string
        self._tokenizer = Tokenizer(string)

        # Prime the tokenizer to obtain the first token
        # which is our lookahead. The lookahead is used
        # for predictive parsing.
        self._lookahead = self._tokenizer.getNextToken()

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
        return {
            'type': 'Program',
            'body': self.NumbericLiteral(),
        }

    '''
    NumericLiteral
        : NUMBER
        ;
    '''
    def NumbericLiteral(self):
        token = self._eat('NUMBER')
        return {'type': 'NumericLiteral', 'value':toNumber(token['value'])}

    # Expects a token of a given type.
    def _eat(self, tokenType):
        token = self._lookahead

        if token == None:
            raise Exception('Unexpected end of input, expected: "%s"'%(tokenType))
        if token['type'] != tokenType:
            raise Exception('Unexpected token: "%s", expected: "%s"'%(token['value'], tokenType))

        # Advance to next token.
        self._lookahead = self._tokenizer.getNextToken()

        return token

def toNumber(s):
    try:
        return int(s)
    except ValueError:
        return float(s)