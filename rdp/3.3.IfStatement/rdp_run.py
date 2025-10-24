from rdp import Parser
from rdp_tests import tests
import json

parser = Parser()

# program = '''
#     let x = 42;

#     if (x) {
#         x = 0;
#     } else {
#         x += 1;
#     }
# '''
# program = '''
#     if (x) if (y) {} else {} else {}
# '''

# For manual tests.
def exec():
    program = '''
        if (x >= 10) {
            x = 0;
        } else {
            x += 1;
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
