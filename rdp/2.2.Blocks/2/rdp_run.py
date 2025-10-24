from rdp import Parser
from rdp_tests import tests

parser = Parser()

# For manual tests.
def exec():
    program = '''
    ;
    '''

    ast = parser.parse(program)
    print(ast)

# Manual test:
exec()

# Test function.
def test(code, expected):
    try:
        got = parser.parse(code)
        assert got == expected
    except AssertionError as e:
        print(f'expected: "{expected}", got: "{got}"\nerror occurs in test: {code}')
        raise e

# Run all tests:
for testRun in tests:
    testRun(test)

print("All assertions passed!")
