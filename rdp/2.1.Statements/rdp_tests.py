literalTests = [
    # NumericLiteral
    lambda test: test('42;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'NumericLiteral',
                    'value': 42,
                }
            }
        ]
    }),

    # StringLiteral
    lambda test: test('"hello";', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'expression':  {
                    'type': 'StringLiteral',
                    'value': 'hello',
                }
            }
        ]
    }),

    # StringLiteral
    lambda test: test("'hello';", {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'expression':  {
                    'type': 'StringLiteral',
                    'value': 'hello',
                }
            }
        ]
    }),
]

statementTests = [
    lambda test: test('''
    /**
    * Documentation comment
    */
    "hello";

    // Number
    42;

    ''', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'expression':  {
                    'type': 'StringLiteral',
                    'value': 'hello',
                }
            },
            {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'NumericLiteral',
                    'value': 42,
                }
            },
        ]
    }),
]

tests = [*literalTests, *statementTests]