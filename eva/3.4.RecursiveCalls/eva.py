from environment import Environment
import re
import operator as op

# Default Global Environment.
GlobalEnvironment = Environment({
    'null': None,
    'true': True,
    'false': False,
    'VERSION': '0.1',
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    '>':op.gt,
    '<':op.lt,
    '>=':op.ge,
    '<=':op.le,
    '=':op.eq,
    'print': lambda *args : print(*args),
})

# Eva interpreter.
class Eva:
    # Creates an Eva instance with the global environment.
    def __init__(self, globalEnv = GlobalEnvironment):
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

        # while expression:
        if exp[0] == 'while':
            _tag, condition, body = exp
            while self.eval(condition, env):
                result = self.eval(body, env)
            return result

        # Function declaration:
        if exp[0] == 'def':
            _tag, name, params, body = exp
            # JIT-transpile to a variable declaration
            varExp = ['var', name, ['lambda', params, body]]
            return self.eval(varExp, env)

        # Lambda function:
        if exp[0] == 'lambda':
            _tag, params, body = exp
            return {
                'params': params,
                'body': body,
                'env': env,
            }

        # Function calls:
        if isinstance(exp, list):
            fn = self.eval(exp[0], env)
            args = [self.eval(arg, env) for arg in exp[1:]]

            # native function
            if callable(fn):
                return fn(*args)

            # user-defined function
            activationRecord = {}
            for index, param in enumerate(fn['params']):
                activationRecord[param] = args[index]

            activationEnv = Environment(activationRecord, fn['env'])

            return self._evalBody(fn['body'], activationEnv)

        raise Exception("Unimplemented: " + str(exp))

    def _evalBlock(self, block, env):
        _, *expressions = block

        result = []
        for exp in expressions:
            result.append(self.eval(exp, env))
        return result[-1]

    def _evalBody(self, body, env):
        if body[0] == 'begin':
            return self._evalBlock(body, env)
        return self.eval(body, env)

def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')

def isVariableName(exp):
    return (type(exp) == str) and re.search(r"^[a-zA-Z_][a-zA-Z_0-9]*|[-+*/<>=]$", exp)





