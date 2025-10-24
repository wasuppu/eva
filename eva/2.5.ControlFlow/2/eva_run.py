from eva import Eva
from environment import Environment
from eva_tests import tests

eva = Eva(Environment({
    'null': None,

    'true': True,
    'false': False,

    'VERSION': '0.1'
}))

def test(eva, code, expected):
    try:
        got = eva.eval(code)
        assert got == expected
    except AssertionError as e:
        print(f'expected: "{expected}", got: "{got}"\nerror occurs in test: {code}')
        raise e
    except Exception as e:
        print(f'error occurs in test: {code}')
        raise e

for code, expected in tests:
    test(eva, code, expected)

print("All assertions passed!")