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
        | IterationStatement
        | FunctionDeclaration
        | ReturnStatement
        | ClassDeclaration
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
        elif self._lookahead['type'] == 'def':
            return self.FunctionDeclaration()
        elif self._lookahead['type'] == 'class':
            return self.ClassDeclaration()
        elif self._lookahead['type'] == 'return':
            return self.ReturnStatement()
        elif (self._lookahead['type'] == 'while' or
                self._lookahead['type'] == 'do' or
                self._lookahead['type'] == 'for'):
            return self.IterationStatement()
        else:
            return self.ExpressionStatement()

    '''
    ClassDeclaration
        : 'class' Identifier OptClassExtends BlockStatement
        ;
    '''
    def ClassDeclaration(self):
        self._eat('class')
        id = self.Identifier()
        superClass = None
        if self._lookahead['type'] == 'extends':
            superClass = self.ClassExtends()
        body = self.BlockStatement()
        return {'type': 'ClassDeclaration', 'id': id, 'superClass': superClass, 'body': body}

    '''
    ClassExtends
        : 'extends' Identifier
        ;
    '''
    def ClassExtends(self):
        self._eat('extends')
        return self.Identifier()

    '''
    FunctionDeclaration
        : 'def' Identifier '(' OptFormalParameterList ')' BlockStatement
        ;
    '''
    def FunctionDeclaration(self):
        self._eat('def')
        name = self.Identifier()

        self._eat('(')
        params = []
        if self._lookahead['type'] != ')':
            params = self.FormalParameterList()
        self._eat(')')

        body = self.BlockStatement()
        return {'type': 'FunctionDeclaration', 'name': name, 'params': params, 'body': body}

    '''
    FormalParameterList
        : Identifier
        | FormalParameterList ',' Identifier
        ;
    '''
    def FormalParameterList(self):
        params = []
        while True:
            params.append(self.Identifier())
            if self._lookahead['type'] == ',':
                self._eat(',')
            else:
                break
        return params

    '''
    ReturnStatement
        : 'return' OptExpression ';'
        ;
    '''
    def ReturnStatement(self):
        self._eat('return')
        argument = None
        if self._lookahead['type'] != ';':
            argument = self.Expression()
        self._eat(';')
        return {'type': 'ReturnStatement', 'argument': argument}

    '''
    IterationStatement
        : WhileStatement
        | DoWhileStatement
        | ForStatement
        ;
    '''
    def IterationStatement(self):
        if self._lookahead['type'] == 'while':
            return self.WhileStatement()
        elif self._lookahead['type'] == 'do':
            return self.DoWhileStatement()
        elif self._lookahead['type'] == 'for':
            return self.ForStatement()

    '''
    WhileStatement
        : 'while' '(' Expression ')' Statement
        ;
    '''
    def WhileStatement(self):
        self._eat('while')
        self._eat('(')
        test = self.Expression()
        self._eat(')')
        body = self.Statement()

        return {'type': 'WhileStatement', 'test': test, 'body': body}

    '''
    DoWhileStatement
        : 'do' Statement 'while' '(' Expression ')' ';'
    '''
    def DoWhileStatement(self):
        self._eat('do')
        body = self.Statement()
        self._eat('while')

        self._eat('(')
        test = self.Expression()
        self._eat(')')
        self._eat(';')

        return {'type': 'DoWhileStatement', 'body': body, 'test': test}

    '''
    ForStatement
        : 'for' '(' OptForStatementInit ';' OptExpression ';' OptExpression ')' Statement
        ;
    '''
    def ForStatement(self):
        self._eat('for')
        self._eat('(')

        init = None
        if self._lookahead['type'] != ';':
            init = self.ForStatementInit()
        self._eat(';')

        test = None
        if self._lookahead['type'] != ';':
            test = self.Expression()
        self._eat(';')

        update = None
        if self._lookahead['type'] != ')':
            update = self.Expression()
        self._eat(')')

        body = self.Statement()

        return {'type': 'ForStatement', 'init': init, 'test': test, 'update': update, 'body': body}

    '''
    ForStatementInit
        : VariableStatementInit
        | Expression
    ;
    '''
    def ForStatementInit(self):
        if self._lookahead['type'] == 'let':
            return self.VariableStatementInit()
        return self.ExpressionList()

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
    VariableStatementInit
        : 'let' VariableDeclarationList
        ;
    '''
    def VariableStatementInit(self):
        self._eat('let')
        declarations = self.VariableDeclarationList()
        return {'type': 'VariableStatement', 'declarations': declarations}

    '''
    VariableStatement
        : VariableStatementInit ';'
        ;
    '''
    def VariableStatement(self):
        variableStatement = self.VariableStatementInit()
        self._eat(';')
        return variableStatement

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
    ExpressionList
        : Expression
        | ExpressionList ',' Expression
        ;
    '''
    def ExpressionList(self):
        expressions = []
        while True:
            expressions.append(self.Expression())
            if self._lookahead['type'] == ',':
                self._eat(',')
            else:
                break
        return expressions

    '''
    Expression
        : AssignmentExpression
        ;
    '''
    def Expression(self):
        return self.AssignmentExpression()

    '''
    AssignmentExpression
        : LogicalORExpression
        | LeftHandSideExpression AssignmentOperator AssignmentExpression
        ;
    '''
    def AssignmentExpression(self):
        left = self.LogicalORExpression()
        if not self._isAssignmentOperator(self._lookahead['type']):
            return left

        return {
            'type': 'AssignmentExpression',
            'operator': self.AssignmentOperator()['value'],
            'left': self._checkValidAssignmentTarget(left),
            'right': self.AssignmentExpression(),
        }

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
    Logical AND expression.
        x && y

    LogicalANDExpression
        : EqualityExpression
        | LogicalANDExpression LOGICAL_AND EqualityExpression
        ;
    '''
    def LogicalANDExpression(self):
        return self._LogicalExpression(self.EqualityExpression, 'LOGICAL_AND')

    '''
    Logical OR expression.
        x || y

    LogicalORExpression
        : LogicalORExpression
        | LogicalORExpression LOGICAL_OR LogicalANDExpression
        ;
    '''
    def LogicalORExpression(self):
        return self._LogicalExpression(self.LogicalANDExpression, 'LOGICAL_OR')

    '''
    EQUALITY_OPERATOR: ==, !=
        x == y, x != y

    EqualityExpression
        : RelationalExpression
        | EqualityExpression EQUALITY_OPERATOR RelationalExpression
        ;
    '''
    def EqualityExpression(self):
        return self._BinaryExpression(self.RelationalExpression, 'EQUALITY_OPERATOR')

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
        : UnaryExpression
        | MultiplicativeExpression MULTIPLICATIVE_OPERATOR PrimaryExpression
        ;
    '''
    def MultiplicativeExpression(self):
        return self._BinaryExpression(self.UnaryExpression, 'MULTIPLICATIVE_OPERATOR')

    '''
    UnaryExpression
        : LeftHandSideExpression
        | ADDITIVE_OPERATOR UnaryExpression
        | LOGICAL_NOT UnaryExpression
        ;
    '''
    def UnaryExpression(self):
        operator = None
        if self._lookahead['type'] == 'ADDITIVE_OPERATOR':
            operator = self._eat('ADDITIVE_OPERATOR')['value']
        elif self._lookahead['type'] == 'LOGICAL_NOT':
            operator = self._eat('LOGICAL_NOT')['value']

        if operator != None:
            return {'type': 'UnaryExpression', 'operator': operator, 'argument': self.UnaryExpression()}

        return self.LeftHandSideExpression()

    '''
    LeftHandSideExpression
        : CallMemberExpression
        ;
    '''
    def LeftHandSideExpression(self):
        return self.CallMemberExpression()

    '''
    CallMemberExpression
        : Super
        | MemberExpression
        | CallExpression
        ;
    '''
    def CallMemberExpression(self):
        # Super Call:
        if self._lookahead['type'] == 'super':
            return self._CallExpression(self.Super())

        # Member part, might be part of call;
        member = self.MemberExpression()

        # See if we have a call expression
        if self._lookahead['type'] == '(':
            return self._CallExpression(member)

        # Simple member expression:
        return member

    '''
    MemberExpression
        : PrimaryExpression
        | MemberExpression '.' Identifier
        | MemberExpression '[' Expression ']'
        ;
    '''
    def MemberExpression(self):
        object = self.PrimaryExpression()

        while self._lookahead['type'] == '.' or self._lookahead['type'] == '[':
            # MemberExpression '.' Identifier
            if self._lookahead['type'] == '.':
                self._eat('.')
                property = self.Identifier()
                object = {'type': 'MemberExpression', 'computed': False, 'object': object, 'property': property}

            # MemberExpression '[' Expression ']'
            if self._lookahead['type'] == '[':
                self._eat('[')
                property = self.Expression()
                self._eat(']')
                object = {'type': 'MemberExpression', 'computed': True, 'object': object, 'property': property}

        return object

    '''
    PrimaryExpression
        : Literal
        | ParenthesizedExpression
        | Identifier
        | ThisExpression
        | NewExpression
        ;
    '''
    def PrimaryExpression(self):
        if self._isLiteral(self._lookahead['type']):
            return self.Literal()

        if self._lookahead['type'] == '(':
            return self.ParenthesizedExpression()
        elif self._lookahead['type'] == 'IDENTIFIER':
            return self.Identifier()
        elif self._lookahead['type'] == 'this':
            return self.ThisExpression()
        elif self._lookahead['type'] == 'new':
            return self.NewExpression()
        else:
            return self.LeftHandSideExpression()

    '''
    NewExpression
        : 'new' MemberExpression Arguments
        ;
    '''
    def NewExpression(self):
        self._eat('new')
        return {'type': 'NewExpression', 'callee': self.MemberExpression(), 'arguments': self.Arguments()}

    '''
    ThisExpression
        : 'this'
        ;
    '''
    def ThisExpression(self):
        self._eat('this')
        return {'type': 'ThisExpression'}

    '''
    Super
        : 'super'
        ;
    '''
    def Super(self):
        self._eat('super')
        return {'type': 'Super'}

    '''
    Identifier
        : IDENTIFIER
        ;
    '''
    def Identifier(self):
        name = self._eat('IDENTIFIER')['value']
        return {'type': 'Identifier', 'name': name}

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
        | BooleanLiteral
        | NullLiteral
        ;
    '''
    def Literal(self):
        if self._lookahead['type'] == 'NUMBER':
            return self.NumbericLiteral()
        elif self._lookahead['type'] == 'STRING':
            return self.StringLiteral()
        elif self._lookahead['type'] == 'true':
            return self.BooleanLiteral(True)
        elif self._lookahead['type'] == 'false':
            return self.BooleanLiteral(False)
        elif self._lookahead['type'] == 'null':
            return self.NullLiteral()
        else:
            raise Exception('Literal: unexpected literal production')

    '''
    BooleanLiteral
        : 'true'
        | 'false'
        ;
    '''
    def BooleanLiteral(self, value):
        if value:
            self._eat('true')
        else:
            self._eat('false')
        return {'type': 'BooleanLiteral', 'value': value}

    '''
    NullLiteral
        : 'null'
        ;
    '''
    def NullLiteral(self):
        self._eat('null')
        return {'type': 'NullLiteral', 'value': None}

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

    '''
    Arguments
        : '(' OptArgumentList ')'
        ;
    '''
    def Arguments(self):
        self._eat('(')

        argumentList = []
        if self._lookahead['type'] != ')':
            argumentList = self.ArgumentList()
        self._eat(')')

        return argumentList

    '''
    ArgumentList
        : AssignmentExpression
        | ArgumentList ',' AssignmentExpression
        ;
    '''
    def ArgumentList(self):
        argumentList = []

        while True:
            argumentList.append(self.AssignmentExpression())
            if self._lookahead['type'] == ',':
                self._eat(',')
            else:
                break

        return argumentList

    '''
    CallExpression
        : Callee Arguments
        ;

    Callee
        : MemberExpression
        | CallExpression
        ;
    '''
    # Generic call expression helper.
    def _CallExpression(self, callee):
        callExpression = {'type': 'CallExpression', 'callee': callee, 'arguments': self.Arguments()}

        if self._lookahead['type'] == '(':
            callExpression = self._CallExpression(callExpression)

        return callExpression

    # Generic helper for LogicalExpression nodes.
    def _LogicalExpression(self, builder, operatorToken):
        left = builder()

        while self._lookahead['type'] == operatorToken:
            operator = self._eat(operatorToken)['value']
            right = builder()
            left = {
                'type': 'LogicalExpression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    # Whether the token is a literal.
    def _isLiteral(self, tokenType):
        return (
                tokenType == 'NUMBER' or
                tokenType == 'STRING' or
                tokenType == 'true' or
                tokenType == 'false' or
                tokenType == 'null'
            )

    # Extra check whether it's valid assignment target.
    def _checkValidAssignmentTarget(self, node):
        if node['type'] == 'Identifier' or node['type'] == 'MemberExpression':
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