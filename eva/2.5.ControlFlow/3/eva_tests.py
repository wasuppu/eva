# Atom:
atomTests = [
    (1, 1),
    ('"Hello"', 'Hello'),
]

# Math:
mathTests = [
    (['+', 1, 5], 6),
    (['+', ['+', 3, 2], 5], 10),
    (['+', ['*', 3, 2], 5], 11),
]

# Variables:
variableTests = [
    (['var', 'x', 10], 10),
    ('x', 10),

    (['var', 'y', 100], 100),
    ('y', 100),

    ('VERSION', '0.1'),

    (['var', 'isUser', 'true'], True),

    (['var', 'z', ['*', 2, 2]], 4),
    ('z', 4),
]

# Blocks:
blockTests = [
    (['begin',
        ['var', 'x', 10],
        ['var', 'y', 20],
        ['+', ['*', 'x', 'y'], 30]
    ], 230),

    (['begin',
        ['var', 'x', 10],
        ['begin',
            ['var', 'x', 20],
            'x'
        ],
        'x'
    ], 10),

    (['begin',
        ['var', 'value', 10],
        ['var', 'result',
            ['begin',
                ['var', 'x', ['+', 'value', 10]],
                'x'
            ]],
        'result'
    ], 20),

    (['begin',
        ['var', 'data', 10],
        ['begin',
            ['set', 'data', 100]],
        'data'
    ], 100),
]

ifTests = [
    (['begin',
        ['var', 'x', 10],
        ['var', 'y', 0],
        ['if', ['>', 'x', 10],
            ['set', 'y', 20],
            ['set', 'y', 30]
        ],
        'y'
    ], 30),
]

whileTests = [
    (['begin',
        ['var', 'counter', 0],
        ['var', 'result', 0],
        ['while', ['<', 'counter', 10],
            ['begin',
                ['set', 'result', ['+', 'result', 1]],
                ['set', 'counter', ['+', 'counter', 1]]
            ],
        ],
        'result'
    ], 10),
]


tests = [*atomTests, *mathTests, *variableTests, *blockTests, *ifTests, *whileTests]