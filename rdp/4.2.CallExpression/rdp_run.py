from rdp import Parser
from rdp_tests import tests
import json

parser = Parser()

# For manual tests.
def exec():
    program = '''
        let s = "Hello, world!";
        let i = 0;
        while (i < s.length) {
            cnosole.log(i, s[i]);
            i += 1;
        }
        square(2);
        getCallback()();
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
