import Type

def exec(eva, exp):
    return eva.tc(exp, None)

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


testcases = [*selfEvalTests, *mathTests, *variableTests]
