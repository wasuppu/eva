import Type

def exec(eva, exp):
    return eva.tc(exp)

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

testcases = [*selfEvalTests]
