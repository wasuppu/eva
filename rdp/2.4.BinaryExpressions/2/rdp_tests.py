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

mathTests = [
    # Addition:
    lambda test: test('''
    2 + 2;
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'BinaryExpression',
                    'operator': '+',
                    'left': {
                            'type': 'NumericLiteral',
                            'value': 2,
                        },
                    'right': {
                            'type': 'NumericLiteral',
                            'value': 2,
                        },
                }
            },
        ]
    }),

    # Nested binary expressions:
    lambda test: test('''
    3 + 2 - 2;
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'BinaryExpression',
                    'operator': '-',
                    'left': {
                        'type': 'BinaryExpression',
                        'operator': '+',
                        'left': {
                                'type': 'NumericLiteral',
                                'value': 3,
                            },
                        'right': {
                                'type': 'NumericLiteral',
                                'value': 2,
                            },
                        },
                    'right': {
                            'type': 'NumericLiteral',
                            'value': 2,
                        },
                }
            },
        ]
    }),

    lambda test: test('''
    2 * 2;
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'BinaryExpression',
                    'operator': '*',
                    'left': {
                            'type': 'NumericLiteral',
                            'value': 2,
                        },
                    'right': {
                            'type': 'NumericLiteral',
                            'value': 2,
                        },
                }
            },
        ]
    }),

    # Precedence of operations:
    lambda test: test('''
    3 + 2 * 2;
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'BinaryExpression',
                    'operator': '+',
                    'left': {
                            'type': 'NumericLiteral',
                            'value': 3,
                        },
                    'right': {
                        'type': 'BinaryExpression',
                        'operator': '*',
                        'left': {
                                'type': 'NumericLiteral',
                                'value': 2,
                            },
                        'right': {
                                'type': 'NumericLiteral',
                                'value': 2,
                            },
                        },
                }
            },
        ]
    }),
]

tests = [*literalTests, *statementTests, *blockTests, *emptyStatementTests, *mathTests]