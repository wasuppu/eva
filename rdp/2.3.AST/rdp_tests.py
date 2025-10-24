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

blockTests = [
    lambda test: test('''
    {
        42;
        "hello";
    }
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'BlockStatement',
                'body': [
                    {
                        'type': 'ExpressionStatement',
                        'expression': {
                            'type': 'NumericLiteral',
                            'value': 42,
                        }
                    },
                    {
                        'type': 'ExpressionStatement',
                        'expression':  {
                            'type': 'StringLiteral',
                            'value': 'hello',
                        }
                    },
                ]
            },
        ]
    }),

    # Empty Block:
    lambda test: test('''
    {
    }
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'BlockStatement',
                'body': [
                ]
            },
        ]
    }),

    # Nested Block:
    lambda test: test('''
    {
        42;
        {
            "hello";
        }
    }
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'BlockStatement',
                'body': [
                    {
                        'type': 'ExpressionStatement',
                        'expression': {
                            'type': 'NumericLiteral',
                            'value': 42,
                        }
                    },
                    {
                        'type': 'BlockStatement',
                        'body': [
                            {
                                'type': 'ExpressionStatement',
                                'expression':  {
                                    'type': 'StringLiteral',
                                    'value': 'hello',
                                }
                            },
                        ]
                    },
                ]
            },
        ]
    }),
]

emptyStatementTests = [
    lambda test: test('''
    ;
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'EmptyStatement',
            },
        ]
    }),
]

tests = [*literalTests, *statementTests, *blockTests, *emptyStatementTests]