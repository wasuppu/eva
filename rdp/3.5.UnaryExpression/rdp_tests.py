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

  # Precedence of operations:
  lambda test: test('''
    (3 + 2) * 2;
    ''',
    {'type': 'Program',
     'body': [
            {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'BinaryExpression',
                    'operator': '*',
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
]

assignmentTests = [
  # Simple assignment:
  lambda test: test('x = 42;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'AssignmentExpression',
          'operator': '=',
          'left': {
            'type': 'Identifier',
            'name': 'x',
          },
          'right': {
            'type': 'NumericLiteral',
            'value': 42,
          },
        },
      },
    ],
  }),

  # Chained assignment:
  lambda test: test('x = y = 42;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'AssignmentExpression',
          'operator': '=',
          'left': {
            'type': 'Identifier',
            'name': 'x',
          },
          'right': {
            'type': 'AssignmentExpression',
            'operator': '=',
            'left': {
              'type': 'Identifier',
              'name': 'y',
            },
            'right': {
              'type': 'NumericLiteral',
              'value': 42,
            },
          },
        },
      },
    ],
  }),
]

variableTests = [
  # Simple variable declaration:
  lambda test: test('let x = 42;', {
    'type': 'Program',
    'body': [
      {
        'type': 'VariableStatement',
        'declarations': [
          {
            'type': 'VariableDeclaration',
            'id': {
              'type': 'Identifier',
              'name': 'x',
            },
            'init': {
              'type': 'NumericLiteral',
              'value': 42,
            },
          },
        ],
      },
    ],
  }),

  # Variable declaration, no 'init':
  lambda test: test('let x;', {
    'type': 'Program',
    'body': [
      {
        'type': 'VariableStatement',
        'declarations': [
          {
            'type': 'VariableDeclaration',
            'id': {
              'type': 'Identifier',
              'name': 'x',
            },
            'init': None,
          },
        ],
      },
    ],
  }),

  # Multiple variable declarations, no 'init':
  lambda test: test('let x, y;', {
    'type': 'Program',
    'body': [
      {
        'type': 'VariableStatement',
        'declarations': [
          {
            'type': 'VariableDeclaration',
            'id': {
              'type': 'Identifier',
              'name': 'x',
            },
            'init': None,
          },
          {
            'type': 'VariableDeclaration',
            'id': {
              'type': 'Identifier',
              'name': 'y',
            },
            'init': None,
          },
        ],
      },
    ],
  }),

  # Multiple variable 'declarations':
  lambda test: test('let x, y = 42;', {
    'type': 'Program',
    'body': [
      {
        'type': 'VariableStatement',
        'declarations': [
          {
            'type': 'VariableDeclaration',
            'id': {
              'type': 'Identifier',
              'name': 'x',
            },
            'init': None,
          },
          {
            'type': 'VariableDeclaration',
            'id': {
              'type': 'Identifier',
              'name': 'y',
            },
            'init': {
              'type': 'NumericLiteral',
              'value': 42,
            },
          },
        ],
      },
    ],
  }),
]

ifTests = [
  lambda test: test(
    '''
    if (x) {
      x = 1;
    } else {
      x = 2;
    }
    ''',
    {
      'type': 'Program',
      'body': [
        {
          'type': 'IfStatement',
          'test': {
            'type': 'Identifier',
            'name': 'x',
          },
          'consequent': {
            'type': 'BlockStatement',
            'body': [
              {
                'type': 'ExpressionStatement',
                'expression': {
                  'type': 'AssignmentExpression',
                  'operator': '=',
                  'left': {
                    'type': 'Identifier',
                    'name': 'x',
                  },
                  'right': {
                    'type': 'NumericLiteral',
                    'value': 1,
                  },
                },
              },
            ],
          },
          'alternate': {
            'type': 'BlockStatement',
            'body': [
              {
                'type': 'ExpressionStatement',
                'expression': {
                  'type': 'AssignmentExpression',
                  'operator': '=',
                  'left': {
                    'type': 'Identifier',
                    'name': 'x',
                  },
                  'right': {
                    'type': 'NumericLiteral',
                    'value': 2,
                  },
                },
              },
            ],
          },
        },
      ],
    },
  ),

  # No else part:
  lambda test: test(
    '''
    if (x) {
      x = 1;
    }

    ''',
    {
      'type': 'Program',
      'body': [
        {
          'type': 'IfStatement',
          'test': {
            'type': 'Identifier',
            'name': 'x',
          },
          'consequent': {
            'type': 'BlockStatement',
            'body': [
              {
                'type': 'ExpressionStatement',
                'expression': {
                  'type': 'AssignmentExpression',
                  'operator': '=',
                  'left': {
                    'type': 'Identifier',
                    'name': 'x',
                  },
                  'right': {
                    'type': 'NumericLiteral',
                    'value': 1,
                  },
                },
              },
            ],
          },
          'alternate': None,
        },
      ],
    },
  ),
]

relationalTests = [
  lambda test: test('x > 0;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'BinaryExpression',
          'operator': '>',
          'left': {
            'type': 'Identifier',
            'name': 'x',
          },
          'right': {
            'type': 'NumericLiteral',
            'value': 0,
          },
        },
      },
    ],
  }),
]

equalityTests = [
  lambda test: test('x > 0 == true;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'BinaryExpression',
          'operator': '==',
          'left': {
            'type': 'BinaryExpression',
            'operator': '>',
            'left': {
              'type': 'Identifier',
              'name': 'x',
            },
            'right': {
              'type': 'NumericLiteral',
              'value': 0,
            },
          },
          'right': {
            'type': 'BooleanLiteral',
            'value': True,
          },
        },
      },
    ],
  }),

  lambda test: test('x >= 0 != false;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'BinaryExpression',
          'operator': '!=',
          'left': {
            'type': 'BinaryExpression',
            'operator': '>=',
            'left': {
              'type': 'Identifier',
              'name': 'x',
            },
            'right': {
              'type': 'NumericLiteral',
              'value': 0,
            },
          },
          'right': {
            'type': 'BooleanLiteral',
            'value': False,
          },
        },
      },
    ],
  }),
]

logicalTests = [
  lambda test: test('x > 0 && y < 1;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'LogicalExpression',
          'operator': '&&',
          'left': {
            'type': 'BinaryExpression',
            'operator': '>',
            'left': {
              'type': 'Identifier',
              'name': 'x',
            },
            'right': {
              'type': 'NumericLiteral',
              'value': 0,
            },
          },
          'right': {
            'type': 'BinaryExpression',
            'operator': '<',
            'left': {
              'type': 'Identifier',
              'name': 'y',
            },
            'right': {
              'type': 'NumericLiteral',
              'value': 1,
            },
          },
        },
      },
    ],
  }),
]

unaryTests = [
  lambda test: test('-x;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'UnaryExpression',
          'operator': '-',
          'argument': {
            'type': 'Identifier',
            'name': 'x',
          },
        },
      },
    ],
  }),

  lambda test: test('!x;', {
    'type': 'Program',
    'body': [
      {
        'type': 'ExpressionStatement',
        'expression': {
          'type': 'UnaryExpression',
          'operator': '!',
          'argument': {
            'type': 'Identifier',
            'name': 'x',
          },
        },
      },
    ],
  }),
]


tests = [*literalTests, *statementTests, *blockTests, *emptyStatementTests, *mathTests,
        *assignmentTests, *variableTests, *ifTests, *relationalTests, *equalityTests, *logicalTests,
        *unaryTests]