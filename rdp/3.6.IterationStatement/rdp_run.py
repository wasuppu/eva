from rdp import Parser
from rdp_tests import tests
import json

parser = Parser()

# For manual tests.
def exec():
    program = '''
        while (x > 10) {
            x -= 1;
        }

        do {
            x -= 1;
        } while (x > 10);

        for (let i = 0, z = 0; i < 10; i += 1) {
            x += i;
        }

        for (i = 0, z = 0; i < 10; i += 1) {
            x += i;
        }

        for (;;) {
            x += i;
        }
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
