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
        : StatementList
        ;
    '''
    def program(self):
        return {'type': 'Program', 'body': self.StatementList()}

    '''
    StatementList
        : Statement
        | StatementList Statement
        ;
    '''
    def StatementList(self, stopLookahead = None):
        statementList = [self.Statement()]
        while self._lookahead != None and self._lookahead['type'] != stopLookahead :
            statementList.append(self.Statement())
        return statementList

    '''
    Statement
        : ExpressionStatement
        | BlockStatement
        | EmptyStatement
        ;
    '''
    def Statement(self):
        if self._lookahead['type'] == ';':
            return self.EmptyStatement()
        elif self._lookahead['type'] == '{':
            return self.BlockStatement()
        else:
            return self.ExpressionStatement()

    '''
    EmptyStatement
        : ';'
        ;
    '''
    def EmptyStatement(self):
        self._eat(';')
        return {'type': 'EmptyStatement'}

    '''
    BlockStatement
        : '{' OptStatementList '}'
        ;
    '''
    def BlockStatement(self):
        self._eat('{')

        # OptStatementList
        if self._lookahead['type'] != '}':
            body = self.StatementList('}')
        else:
            body = []

        self._eat('}')
        return {'type': 'BlockStatement', 'body': body}

    '''
    ExpressionStatement
        : Expression ';'
        ;
    '''
    def ExpressionStatement(self):
        expression = self.Expression()
        self._eat(';')
        return {'type': 'ExpressionStatement', 'expression': expression}

    '''
    Expression
        : AdditiveExpression
        ;
    '''
    def Expression(self):
        return self.AdditiveExpression()

    '''
    AdditiveExpression
        : MultiplicativeExpression
        | AdditiveExpression ADDITIVE_OPERATOR Literal
        ;
    '''
    def AdditiveExpression(self):
        left = self.MultiplicativeExpression()

        while self._lookahead['type'] == 'ADDITIVE_OPERATOR':
            operator = self._eat('ADDITIVE_OPERATOR')['value']
            right = self.MultiplicativeExpression()
            left = {
                'type': 'BinaryExpression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    '''
    MultiplicativeExpression
        : PrimaryExpression
        | MultiplicativeExpression MULTIPLICATIVE_OPERATOR PrimaryExpression
        ;
    '''
    def MultiplicativeExpression(self):
        left = self.PrimaryExpression()

        while self._lookahead['type'] == 'MULTIPLICATIVE_OPERATOR':
            operator = self._eat('MULTIPLICATIVE_OPERATOR')['value']
            right = self.PrimaryExpression()
            left = {
                'type': 'BinaryExpression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    '''
    PrimaryExpression
        : Literal
        | ParenthesizedExpression
        ;
    '''
    def PrimaryExpression(self):
        if self._lookahead['type'] == '(':
            return self.ParenthesizedExpression()
        else:
            return self.Literal()

    '''
    ParenthesizedExpression
        : '(' Expression ')'
        ;
    '''
    def ParenthesizedExpression(self):
        self._eat('(')
        expression = self.Expression()
        self._eat(')')
        return expression

    '''
    Literal
        : NumericLiteral
        | StringLiteral
        ;
    '''
    def Literal(self):
        if self._lookahead['type'] == 'NUMBER':
            return self.NumbericLiteral()
        elif self._lookahead['type'] == 'STRING':
            return self.StringLiteral()
        else:
            raise Exception('Literal: unexpected literal production')

    '''
    StringLiteral
        : STRING
        ;
    '''
    def StringLiteral(self):
        token = self._eat('STRING')
        return {'type': 'StringLiteral', 'value':token['value'][1:-1]}

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