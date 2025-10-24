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
            return self.eval(exp[1], env) + self.eval(exp[2], env)

        if exp[0] == '*':
            return self.eval(exp[1], env) * self.eval(exp[2], env)

        # Comparision operations:
        if exp[0] == '>':
            return self.eval(exp[1], env) > self.eval(exp[2], env)
        if exp[0] == '>=':
            return self.eval(exp[1], env) >= self.eval(exp[2], env)
        if exp[0] == '<':
            return self.eval(exp[1], env) < self.eval(exp[2], env)
        if exp[0] == '<=':
            return self.eval(exp[1], env) <= self.eval(exp[2], env)
        if exp[0] == '=':
            return self.eval(exp[1], env) == self.eval(exp[2], env)

        # Block: sequence of expressions:
        if exp[0] == 'begin':
            blockEnv = Environment({}, env)
            return self._evalBlock(exp, blockEnv)

        # Variable declaration:
        if exp[0] == 'var':
            _, name, value = exp
            return env.define(name, self.eval(value, env))

        # Assign value to variable
        if exp[0] == 'set':
            _, name, value = exp
            return env.assign(name, self.eval(value, env))

        # Variable access:
        if isVariableName(exp):
            return env.lookup(exp)

        # if expression:
        if exp[0] == 'if':
            _tag, condition, consequent, alternate = exp
            if self.eval(condition, env):
                return self.eval(consequent, env)
            return self.eval(alternate, env)

        raise Exception("Unimplemented: " + str(exp))

    def _evalBlock(self, block, env):
        _, *expressions = block

        result = []
        for exp in expressions:
            result.append(self.eval(exp, env))
        return result[-1]


def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')

def isVariableName(exp):
    return (type(exp) == str) and re.search(r"^[a-zA-Z][a-zA-Z_0-9]*$", exp)



