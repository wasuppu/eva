from environment import Environment
import re

# Eva interpreter.
class Eva:
    # Creates an Eva instance with the global environment.
    def __init__(self, globalEnv = Environment()):
        self.env = globalEnv

    # Evaluates an expression in the given environment.
    def eval(self, exp, env = None):
        if env == None:
            env = self.env

        # Self-evaluating expressions:
        if isNumber(exp):
            return exp

        if isString(exp):
            return exp[1:-1]

        # Math operations:
        if exp[0] == '+':
            return self.eval(exp[1]) + self.eval(exp[2])

        if exp[0] == '*':
            return self.eval(exp[1]) * self.eval(exp[2])

        # Variable declaration:
        if exp[0] == 'var':
            _, name, value = exp
            return env.define(name, value)

        # Variable access:
        if isVariableName(exp):
            return env.lookup(exp)

        raise Exception("Unimplemented: " + str(exp))


def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')

def isVariableName(exp):
    return (type(exp) == str) and re.search(r"^[a-zA-Z][a-zA-Z_0-9]*$", exp)


# Test:
eva = Eva(Environment({
    'null': None,

    'true': True,
    'false': False,

    'VERSION': '0.1'
}))

assert eva.eval(1) == 1
assert eva.eval('"Hello"') == "Hello"

# Math:
assert eva.eval(['+', 1, 5]) == 6
assert eva.eval(['+', ['+', 3, 2], 5]) == 10
assert eva.eval(['+', ['*', 3, 2], 5]) == 11

# Variables:
assert eva.eval(['var', 'x', 10]) == 10
assert eva.eval('x') == 10

assert eva.eval(['var', 'y', 100]) == 100
assert eva.eval('y') == 100

assert eva.eval('VERSION') == '0.1'

assert eva.eval(['var', 'isUser', 'true']) == True
assert eva.eval(['var', 'z', ['*', 2, 2]]) == 4
assert eva.eval('z') == 4

print("All assertions passed!")


