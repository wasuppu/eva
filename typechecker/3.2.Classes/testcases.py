import Type
from sexp import Sexp
# from EvaTC import EvaTC

evaParser = Sexp()

def exec(eva, exp):
    if isinstance(exp, str):
        exp = evaParser.parse(f"(begin {exp})")
    return eva.tcGlobal(exp)

def test(eva, exp, expected):
    # eva = EvaTC()
    actual = exec(eva, exp)
    try:
        assert actual.equals(expected) == True
    except AssertionError as e:
        print(f"Expected: {expected} type for {exp}, but got {actual}.")
        raise e

selfEvalTests = [
    lambda eva: test(eva, 1, Type.number),
    lambda eva: test(eva, '"hello"', Type.string),
    lambda eva: test(eva, True, Type.boolean),
    lambda eva: test(eva, False, Type.boolean),
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

ifTests = [
    lambda eva: test(eva,
    '''
    (<= 1 10)
    ''',
    Type.boolean),

    # If expression: both branches should return the same type:
    lambda eva: test(eva,
    '''
    (var x 10)
    (var y 20)

    (if (<= x 10)
      (set y 1)
      (set y 2))
    y
    ''',
    Type.number),
]

whileTests = [
    # While expression:
    lambda eva: test(eva,
    '''
    (var x 10)
    (while (!= x 0)
      (set x (- x 1)))
    x
    ''',
    Type.number),
]

userDefinedFunctionTests = [
    # Simple body
    lambda eva: test(eva,
    '''
    (def square ((x number)) -> number
      (* x x))
    (square 2)
    ''',
    Type.number),

    # Complex body
    lambda eva: test(eva,
    '''
    (def calc ((x number) (y number)) -> number
      (begin
        (var z 30)
        (+ (* x y) z)
      ))
    (calc 10 20)
    ''',
    Type.number),

    # Closure:
    lambda eva: test(eva,
    '''
    (var value 100)
    (def calc ((x number) (y number)) -> Fn<number<number>>
      (begin
        (var z (+ x y))
        (def inner ((foo number)) -> number
          (+ (+ foo z) value))
        inner
      ))
    (var fn (calc 10 20))
    (fn 30)
    ''',
    Type.number),

    # Recursive function:
    lambda eva: test(eva,
    '''
    (def factorial ((x number)) -> number
      (if (== x 1)
        1
        (* x (factorial (- x 1)))))

    (factorial 5)
    ''',
    Type.number),
]

buildInFunctionTests = [
    lambda eva: test(eva, '(sum 1 5)', Type.number),
    lambda eva: test(eva, '(sum (square 2) 4)', Type.number),
]

lambdaFunctionTests = [
    # Lambda function:
    lambda eva: test(eva,
    '''
    (lambda ((x number)) -> number (* x x))
    ''',
    Type.fromString('Fn<number<number>>')),

    # Pass lambda as a callback
    lambda eva: test(eva,
    '''
    (def onClick ((callback Fn<number<number>>)) -> number
      (begin
        (var x 10)
        (var y 20)
        (callback (+ x y))))

    (onClick (lambda ((data number)) -> number (* data 10)))
    ''',
    Type.number),

    # Immediately-invoked lambda expression - IILE:
    lambda eva: test(eva,
    '''
    ((lambda ((x number)) -> number (* x x)) 2)
    ''',
    Type.number),

    # Save lambda to a variable:
    lambda eva: test(eva,
    '''
    (var square (lambda ((x number)) -> number (* x x)))
    (square 2)
    ''',
    Type.number),
]

aliasTests = [
    lambda eva: exec(eva,
    '''
    (type int number)
    (type ID int)
    (type Index ID)
    '''),

    lambda eva: test(eva,
    '''
    (def square ((x int)) -> int (* x x))
    (square 2)
    ''',
    Type.int),

    lambda eva: test(eva,
    '''
    (def promote ((userID ID)) -> ID (+ 1 userID))
    (promote 1)
    ''',
    Type.ID),

    lambda eva: test(eva,
    '''
    (var (x Index) 1)
    x
    ''',
    Type.Index),

    lambda eva: test(eva,
    '''
    (var (x Index) 1)
    x
    ''',
    Type.Index),

    lambda eva: test(eva,
    '''
    x
    ''',
    Type.ID),

    lambda eva: test(eva,
    '''
    x
    ''',
    Type.int),
]

classTests = [
    lambda eva: test(eva,
    '''
    (class Point null
      (begin
        (var (x number) 0)
        (var (y number) 0)
        (def constructor ((self Point) (x number) (y number)) -> Point
          (begin
            // (set (prop self x) x)
            // (set (prop self y) y)
            self))
        (def calc ((self Point)) -> number
          1)))
          //(+ (prop self x) (prop self y)))))
    // (var (p Point) (new Point 10 20))
    // ((prop p calc) p)
    1
    ''',
    Type.number),
]

testcases = [*selfEvalTests, *mathTests, *variableTests, *blockTests, *ifTests, *whileTests,
             *userDefinedFunctionTests, *buildInFunctionTests, *lambdaFunctionTests, *aliasTests, *classTests]