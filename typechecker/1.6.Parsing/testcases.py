import Type
from sexp import Sexp

evaParser = Sexp()

def exec(eva, exp):
    if isinstance(exp, str):
        exp = evaParser.parse(f"(begin {exp})")
    return eva.tcGlobal(exp)

def test(eva, exp, expected):
    actual = exec(eva, exp)
    try:
        assert actual.equals(expected) == True
    except AssertionError as e:
        print(f"Expected: {expected} type for {exp}, but got {actual}.")
        raise e

selfEvalTests = [
    lambda eva: test(eva, 1, Type.number),
    lambda eva: test(eva, '"hello"', Type.string),
]

mathTests = [
    # Math.
    lambda eva: test(eva, ['+', 2, 3], Type.number),
    lambda eva: test(eva, ['-', 1, 5], Type.number),
    lambda eva: test(eva, ['*', 4, 3], Type.number),
    lambda eva: test(eva, ['/', 2, 3], Type.number),

    # String concat.
    lambda eva: test(eva, ['+', '"Hello, "', '"world!"'], Type.string),
]

variableTests = [
    # Variable declaration:
    lambda eva: test(eva, ['var', 'x', 10], Type.number),

    # Variable declaration with type check:
    lambda eva: test(eva, ['var', ['y', 'number'], 10], Type.number),
    lambda eva: test(eva, ['var', ['y', 'string'], '"foo"'], Type.string),
    lambda eva: test(eva, ['var', ['y', 'number'], 'x'], Type.number),

    # Variable access:
    lambda eva: test(eva, 'x', Type.number),
    lambda eva: test(eva, 'y', Type.number),

    # Global variable:
    lambda eva: test(eva, 'VERSION', Type.string),
]

blockTests = [
    # Block: sequence of expressions.
    lambda eva: test(eva,
        ['begin',
            ['var', 'x', 10],
            ['var', 'y', 20],
            ['+', ['*', 'x', 10], 'y']],
    Type.number),

    # Block: local scope.
    lambda eva: test(eva,
        ['begin',
            ['var', 'x', 10],
            ['begin',
                ['var', 'x', '"hello"'],
                ['+', 'x', '"world"']],
            ['-', 'x', 5]],
    Type.number),

    lambda eva: test(eva,
        ['begin',
            ['var', 'x', 10],
            ['begin',
                ['var', 'y', 20],
                ['+', 'x', 'y']],
            ['-', 'x', 5]],
    Type.number),

    # Block: variable update.
    lambda eva: test(eva,
        ['begin',
            ['var', 'x', 10],
            # ['set', 'x', '"foo"'], # should raise exception
            ['begin',
                ['var', 'y', 20],
                ['set', 'x', ['+', 'x', 'y']]],
            ['-', 'x', 5]
        ],
    Type.number),

    lambda eva: test(eva,
    '''
    (begin
      (var x 10)
      (var y 20)
      (+ (* x 10) y))
    ''',
    Type.number),

    lambda eva: exec(eva, '(var x 10)'),

    lambda eva: test(eva,
    '''
    (var x 10)
    (var y 20)
    (+ (* x 10) y)
    ''',
    Type.number),
]

testcases = [*selfEvalTests, *mathTests, *variableTests, *blockTests]
