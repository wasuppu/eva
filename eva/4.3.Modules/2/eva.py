from environment import Environment
from transformer import Transformer
import re
import os
import operator as op
from sexp import Sexp

parser = Sexp()

# Default Global Environment.
GlobalEnvironment = Environment({
    'null': None,
    'true': True,
    'false': False,
    'VERSION': '0.1',
    '+': op.add,
    '-': lambda op1, op2 = None : op1 - op2 if op2 else -op1,
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
        self._transformer = Transformer()

    # Evaluates global code wrapping into a block.
    def evalGlobal(self, expressions):
        return self._evalBlock(expressions, self.env)

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
            _, ref, value = exp

            # Assignment to a property:
            if ref[0] == 'prop':
                _tag, instance, propName = ref
                instanceEnv = self.eval(instance, env)
                return instanceEnv.define(propName, self.eval(value, env))

            # Simple assignment:
            return env.assign(ref, self.eval(value, env))

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
            # JIT-transpile to a variable declaration
            varExp = self._transformer.transformDefToVarLambda(exp)
            return self.eval(varExp, env)

        # Switch expression: (switch (cond1, block1) ... )
        # Syntactic sugar for nested if-expressions
        if exp[0] == 'switch':
            ifExp = self._transformer.transformSwitchToIf(exp)
            return self.eval(ifExp, env)

        # For loop: (for init condition modifier body)
        # Syntactic sugar for: (begin init (while condition (begin body modifier)))
        if exp[0] == 'for':
            whileExp = self._transformer.transformForToWhile(exp)
            return self.eval(whileExp, env)

        if exp[0] == '++':
            setExp = self._transformer.transformIncToSet(exp)
            return self.eval(setExp, env)
        if exp[0] == '--':
            setExp = self._transformer.transformDecToSet(exp)
            return self.eval(setExp, env)
        if exp[0] == '+=':
            setExp = self._transformer.transformIncValToSet(exp)
            return self.eval(setExp, env)
        if exp[0] == '-=':
            setExp = self._transformer.transformDecValToSet(exp)
            return self.eval(setExp, env)
        if exp[0] == '*=':
            setExp = self._transformer.transformMulValToSet(exp)
            return self.eval(setExp, env)
        if exp[0] == '/=':
            setExp = self._transformer.transformDivValToSet(exp)
            return self.eval(setExp, env)

        # Lambda function:
        if exp[0] == 'lambda':
            _tag, params, body = exp
            return {
                'params': params,
                'body': body,
                'env': env,
            }

        # class declaration: (class <Name> <Parent> <Body>)
        if exp[0] == 'class':
            _tag, name, parent, body = exp

            # A class is an environment:
            # a storage of methods and shared properties.
            parentEnv = self.eval(parent, env) or env

            classEnv = Environment({}, parentEnv)

            # Body is evaluted in the class environment.
            self._evalBody(body, classEnv)

            # Class is accessible by name.
            return env.define(name, classEnv)

        # Super expressions: (super <ClassName>)
        if exp[0] == 'super':
            _tag, className = exp
            return self.eval(className, env).parent

        # Class instantiation: (new <Class> <Arguments>...)
        if exp[0] == 'new':
            classEnv = self.eval(exp[1], env)

            # An instance of a class is an environment:
            # The `parent` component of the instance environment is set to its class.
            instanceEnv = Environment({}, classEnv)
            args = [self.eval(arg, env) for arg in exp[2:]]
            self._callUserDefinedFunction(classEnv.lookup('constructor'), [instanceEnv, *args])

            return instanceEnv

        # Property access: (prop <instance> <name>)
        if exp[0] == 'prop':
            _tag, instance, name = exp
            instanceEnv = self.eval(instance, env)
            return instanceEnv.lookup(name)

        # Module declaration: (module <name> <body>)
        if exp[0] == 'module':
            _tag, name, body = exp
            moduleEnv = Environment({}, env)
            self._evalBody(body, moduleEnv)
            return env.define(name, moduleEnv)

        # Module import: (import <name>)
        if exp[0] == 'import':
            _tag, *fnames, name = exp
            dirname = os.path.dirname(__file__)

            with open(f'{dirname}/modules/{name}.eva', 'r') as f:
                moduleSrc = f.read()

            body = parser.parse('(begin %s)'%(moduleSrc))

            if fnames != []:
                for fname in fnames[0]:
                    for fn in body:
                        if fname in fn:
                            self.eval(fn, self.env)

            moduleExp = ['module', name, body]
            return self.eval(moduleExp, self.env)

        # Function calls:
        if isinstance(exp, list):
            fn = self.eval(exp[0], env)
            args = [self.eval(arg, env) for arg in exp[1:]]

            # native function
            if callable(fn):
                return fn(*args)

            # user-defined function
            return self._callUserDefinedFunction(fn, args)

        raise Exception("Unimplemented: " + str(exp))

    def _callUserDefinedFunction(self, fn, args):
        activationRecord = {}
        for index, param in enumerate(fn['params']):
            activationRecord[param] = args[index]

        activationEnv = Environment(activationRecord, fn['env'])

        return self._evalBody(fn['body'], activationEnv)

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





