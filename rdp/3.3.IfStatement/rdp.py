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
        | VariableStetement
        | IfStatement
        ;
    '''
    def Statement(self):
        if self._lookahead['type'] == ';':
            return self.EmptyStatement()
        elif self._lookahead['type'] == 'if':
            return self.IfStatement()
        elif self._lookahead['type'] == '{':
            return self.BlockStatement()
        elif self._lookahead['type'] == 'let':
            return self.VariableStatement()
        else:
            return self.ExpressionStatement()

    '''
    IfStatement
       : 'if' '(' Expression ')' Statement
       | 'if' '(' Expression ')' Statement 'else' Statement
       ;
    '''
    def IfStatement(self):
        self._eat('if')
        self._eat('(')
        test = self.Expression()
        self._eat(')')

        consequent = self.Statement()

        alternate = None
        if self._lookahead != None and self._lookahead['type'] == 'else':
            self._eat('else')
            alternate = self.Statement()

        return {'type': 'IfStatement', 'test': test, 'consequent': consequent, 'alternate': alternate}

    '''
    VariableStatement
        : 'let' VariableDeclarationList ';'
        ;
    '''
    def VariableStatement(self):
        self._eat('let')
        declarations = self.VariableDeclarationList()
        self._eat(';')
        return {'type': 'VariableStatement', 'declarations': declarations}

    '''
    VariableDeclarationList
        : VariableDeclaration
        | VariableDeclarationList ',' VariableDeclaration
        ;
    '''
    def VariableDeclarationList(self):
        declarations = []
        while True:
            declarations.append(self.VariableDeclaration())
            if self._lookahead['type'] == ',':
                self._eat(',')
            else:
                break
        return declarations

    '''
    VariableDeclaration
        : Identifier OptVariableInitializer
        ;
    '''
    def VariableDeclaration(self):
        id = self.Identifier()
        init = None
        if self._lookahead['type'] != ';' and self._lookahead['type'] != ',':
            init = self.VariableInitializer()
        return {'type': 'VariableDeclaration', 'id': id, 'init': init}

    '''
    VariableInitializer
       : SIMPLE_ASSIGN AssignmentExpression
       ;
    '''
    def VariableInitializer(self):
        self._eat('SIMPLE_ASSIGN')
        return self.AssignmentExpression()

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
        : AssignmentExpression
        ;
    '''
    def Expression(self):
        return self.AssignmentExpression()

    '''
    AssignmentExpression
        : RelationalExpression
        | LeftHandSideExpression AssignmentOperator AssignmentExpression
        ;
    '''
    def AssignmentExpression(self):
        left = self.RelationalExpression()

        if not self._isAssignmentOperator(self._lookahead['type']):
            return left

        return {
            'type': 'AssignmentExpression',
            'operator': self.AssignmentOperator()['value'],
            'left': self._checkValidAssignmentTarget(left),
            'right': self.AssignmentExpression(),
        }

    '''
    LeftHandSideExpression
        : Identifier
        ;
    '''
    def LeftHandSideExpression(self):
        return self.Identifier()

    '''
    Identifier
        : IDENTIFIER
        ;
    '''
    def Identifier(self):
        name = self._eat('IDENTIFIER')['value']
        return {'type': 'Identifier', 'name': name}

    '''
    AssignmentOperator
      : SIMPLE_ASSIGN
      | COMPLEX_ASSIGN
      ;
    '''
    def AssignmentOperator(self):
        if self._lookahead['type'] == 'SIMPLE_ASSIGN':
            return self._eat('SIMPLE_ASSIGN')
        return self._eat('COMPLEX_ASSIGN')

    '''
    RELATIONAL_OPERATOR: >, >=, <, <=
        x > y, x >= y, x < y, x <= y

    RelationalExpression
        : AdditiveExpression
        | RelationalExpression RELATIONAL_OPERATOR AdditiveExpression
        ;
    '''
    def RelationalExpression(self):
        return self._BinaryExpression(self.AdditiveExpression, 'RELATIONAL_OPERATOR')

    '''
    AdditiveExpression
        : MultiplicativeExpression
        | AdditiveExpression ADDITIVE_OPERATOR Literal
        ;
    '''
    def AdditiveExpression(self):
        return self._BinaryExpression(self.MultiplicativeExpression, 'ADDITIVE_OPERATOR')

    '''
    MultiplicativeExpression
        : PrimaryExpression
        | MultiplicativeExpression MULTIPLICATIVE_OPERATOR PrimaryExpression
        ;
    '''
    def MultiplicativeExpression(self):
        return self._BinaryExpression(self.PrimaryExpression, 'MULTIPLICATIVE_OPERATOR')

    '''
    PrimaryExpression
        : Literal
        | ParenthesizedExpression
        | LeftHandSideExpression
        ;
    '''
    def PrimaryExpression(self):
        if self._isLiteral(self._lookahead['type']):
            return self.Literal()

        if self._lookahead['type'] == '(':
            return self.ParenthesizedExpression()
        else:
            return self.LeftHandSideExpression()

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

    # Whether the token is a literal.
    def _isLiteral(self, tokenType):
        return tokenType == 'NUMBER' or tokenType == 'STRING'

    # Extra check whether it's valid assignment target.
    def _checkValidAssignmentTarget(self, node):
        if node['type'] == 'Identifier':
            return node
        raise Exception('Invalid left-hand side in assignment expression')

    # Whether the token is an assignment operator.
    def _isAssignmentOperator(self, tokenType):
        return tokenType == 'SIMPLE_ASSIGN' or tokenType == 'COMPLEX_ASSIGN'

    # Generic binary expression
    def _BinaryExpression(self, builder, operatorToken):
        left = builder()

        while self._lookahead['type'] == operatorToken:
            operator = self._eat(operatorToken)['value']
            right = builder()
            left = {
                'type': 'BinaryExpression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

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