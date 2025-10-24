from rdp import Parser
from rdp_tests import tests
import json

parser = Parser()

# For manual tests.
def exec():
    program = '''
        let y;
        let a, b;
        let c, d = 10;
        let x = 42;
        let foo = bar = 10;
        r = 10;
    '''

    ast = parser.parse(program)
    print(json.dumps(ast, indent=2))

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
