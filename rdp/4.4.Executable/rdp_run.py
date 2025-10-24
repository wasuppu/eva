from rdp import Parser
from rdp_tests import tests
import json

parser = Parser()

# For manual tests.
def exec():
    program = '''
        class Point {
            def constructor(x, y) {
                this.x = x;
                this.y = y;
            }

            def calc() {
                return this.x + this.y;
            }
        }

        class Point3D extends Point {
            def constructor(x, y, z) {
                super(x, y);
                this.z = z;
            }

            def calc() {
                return super() + this.z;
            }
        }

        let p = new Point3D(10, 20, 30);
        p.calc();
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
