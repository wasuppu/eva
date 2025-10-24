import Type
import re
from TypeEnvironment import TypeEnvironment

# Typed Eva: static typecheker.
class EvaTC:
    # Create the Global TypeEnvironment per Eva instance.
    def __init__(self):
        self._global = self._createGlobal()

    # Evaluates global code wrapping into a block.
    def tcGlobal(self, exp):
        return self._tcBody(exp, self._global)

    # Checks body (global or function).
    def _tcBody(self, body, env):
        if isinstance(body, list) and body[0] == 'begin':
            return self._tcBlock(body, env)
        return self.tc(body, env)

    # Infers and validates type of an expression.
    def tc(self, exp, env):
        if env == None:
            env = self._global

    # Self-evaluating:

        # Numbers
        if isNumber(exp):
            return Type.number

        # Strings
        if isString(exp):
            return Type.string

        # Boolean
        if isBoolean(exp):
            return Type.boolean

        # Math operations:
        if isBinary(exp):
            return self._binary(exp, env)

        # Boolean binary:
        if isBooleanBinary(exp):
            return self._booleanBinary(exp, env)

        # Type declaration/alias: (type <name> <base>)
        if exp[0] == 'type':
            _tag, name, base = exp

            # Union type: (or number string)
            if base[0] == 'or':
                options = base[1:]
                optionTypes = list(map(lambda option: Type.fromString(option), options))

                union = Type.Union(name, optionTypes)
                setattr(Type, name, union)
                return union
            else:
                 # Type alias:
                if hasattr(Type, name):
                    raise f"Type {name} is already defined: {Type.name}."

                if not hasattr(Type, base):
                    raise f"Type {base} is not defined."

                typ = Type.Alias(name, getattr(Type, base))
                setattr(Type, name, typ)
                return typ

        # Class declaration: (class <Name> <Super> <Body>)
        if exp[0] == 'class':
            _tag, name, superClassName, body = exp

            # Resolve super:
            superClass = getattr(Type, superClassName)

            # New class (type):
            classType = Type.Class(name, superClass)

            # Class is accessible by name.
            setattr(Type, name, env.define(name, classType))

            # Body is evaluated in the class environment.
            self._tcBody(body, classType.env)

            return classType

        # Class instantiation: (new <Class> <Arguments>...)
        if exp[0] == 'new':
            _tag, className, *argValues = exp
            classType = getattr(Type, className)

            if className == None:
                raise Exception(f"Unknown class {name}.")

            argTypes = list(map(lambda arg: self.tc(arg, env), argValues))

            return self._checkFunctionCall(classType.getField('constructor'), [classType, *argTypes], env, exp)

        # Super expressions: (super <ClassName>)
        if exp[0] == 'super':
            _tag, className = exp

            classType = getattr(Type, className)

            if classType == None:
                raise Exception(f"Unknown class {name}.")

            return classType.superClass

        # Property access: (prop <instance> <name>)
        if exp[0] == 'prop':
            _tag, instance, name = exp

            instanceType = self.tc(instance, env)

            return instanceType.getField(name)

        # Variable declaration: (var x 10)
        # With typecheck: (var (x number) "foo") # error
        if exp[0] == 'var':
            _tag, name, value = exp

            # Infer actual type:
            valueType = self.tc(value, env)

            # With type check:
            if isinstance(name, list):
                varName, typeStr = name

                expectedType = Type.fromString(typeStr)

                # Check the type:
                self._expect(valueType, expectedType, value, exp)

                return env.define(varName, expectedType)

            # Simple name:
            return env.define(name, valueType)

        # Variable access: foo
        if isVariableName(exp):
            return env.lookup(exp)

        # Variable update: (set x 10)
        if exp[0] == 'set':
            _, ref, value = exp

            # 1. Assignment to a property
            if ref[0] == 'prop':
                _tag, instance, propName = ref
                instanceType = self.tc(instance, env)

                valueType = self.tc(value, env)
                propType = instanceType.getField(propName)

                return self._expect(valueType, propType, value, exp)

            # 2. Simple assignment:

            # The type of the new value should match to the
            # previous type when the variable was defined:

            valueType = self.tc(value, env)
            varType = self.tc(ref, env)

            return self._expect(valueType, varType, value, exp)

        # Block: sequence of expressions
        if exp[0] == 'begin':
            blockEnv = TypeEnvironment({}, env)
            return self._tcBlock(exp, blockEnv)

        # if-expression:
        #
        #    Γ ⊢ e1 : boolean  Γ ⊢ e2 : t  Γ ⊢ e3 : t
        #   ___________________________________________
        #
        #           Γ ⊢ (if e1 e2 e3) : t
        #
        # Both branches should return the same time t.
        if exp[0] == 'if':
            _tag, condition, consequent, alternate = exp

            # Boolean condition:
            t1 = self.tc(condition, env)
            self._expect(t1, Type.boolean, condition, exp)

            # Initially, environment used to tc consequent part is the same as the main env,
            # however can be updated for the union type with type casting:
            consequentEnv = env

            # Check if the condition is a type casting rule.
            # This is used with union types to make a type concrete:
            # (if (== (typeof foo) "string") ...)
            if self._isTypeCastCondition(condition):
                name, specificType = self._getSpecifiedType(condition)

                # Update environment with the concrete type for this name:
                consequentEnv = TypeEnvironment({name: Type.fromString(specificType)}, env)

            t2 = self.tc(consequent, consequentEnv)
            t3 = self.tc(alternate, env)

            # Same types for both branches:
            return self._expect(t3, t2, exp, exp)

        # While expression:
        if exp[0] == 'while':
            _tag, condition, body = exp

            # Boolean condition:
            t1 = self.tc(condition, env)
            self._expect(t1, Type.boolean, condition, exp)

            return self.tc(body, env)

        # Function declaration: (def square ((x number)) -> number (* x x))
        # Syntactic sugar for: (var square (lambda ((x number)) -> number (* x x)))
        if exp[0] == 'def':
            # Transpile to a variable declaration:
            varExp = self._transformDefToVarLambda(exp)
            name = exp[1]
            params = exp[2]
            returnTypeStr = exp[4]

            # We have to extend environment with the function name *before* evaluating the body
            # this is need to support recursive function calls:
            paramTypes = list(map(lambda param: Type.fromString(param[1]), params)) # param: [name, type]

            # Predefine from the signature:
            env.define(name, Type.Function(None, paramTypes, Type.fromString(returnTypeStr)))

            # Delegate to lambda:
            return self.tc(varExp, env)

        # Lambda function:
        if exp[0] == 'lambda':
            _tag, params, _retDel, returnTypeStr, body = exp
            return self._tcFunction(params, returnTypeStr, body, env)

        # Function call.
        if isinstance(exp, list):
            fn = self.tc(exp[0], env)
            argValues = exp[1:]

            # Passed arguments:
            argTypes = list(map(lambda arg: self.tc(arg, env), argValues))
            return self._checkFunctionCall(fn, argTypes, env, exp)

        raise Exception(f"Unknown type for expression {exp}.")

    # Transforms def to var-lambda:
    def _transformDefToVarLambda(self, exp):
        _tag, name, params, _retDel, returnTypeStr, body = exp
        return ['var', name, ['lambda', params, _retDel, returnTypeStr, body]]

    # Whether the if-condition is type casting/specification.
    # This is used with union types to make a type concrete:
    # (if (== (typeof foo) "string") ...)
    def _isTypeCastCondition(self, condition):
        op, lhs, _type = condition
        return op == '==' and lhs[0] == 'typeof'

    # Returns specific type after casting.
    # This is used with union types to make a type concrete:
    # (if (== (typeof foo) "string") ...)
    def _getSpecifiedType(self, condition):
        _op, [_typeof, name], specificType = condition

        # Return name and the new type (stripping quotes).
        return [name, specificType[1:-1]]

    # Checks function call.
    def _checkFunctionCall(self, fn, argTypes, env, exp):
        # Check arity:
        if len(fn.paramTypes) != len(argTypes):
            raise Exception(f"Function {exp[0]} {fn.getName()} expects {len(fn.paramTypes)} arguments, {len(argTypes)} given in {exp}.")

        # Check if argument types match the parameter types:
        for index in range(0, len(argTypes)):
            if fn.paramTypes[index] == Type.any:
                break
            argType = argTypes[index]
            self._expect(argType, fn.paramTypes[index], argTypes[index], exp)

        return fn.returnType

    # Checks function body.
    def _tcFunction(self, params, returnTypeStr, body, env):
        returnType = Type.fromString(returnTypeStr)

        # Parameters environment and types:
        paramsRecord = {}
        paramTypes = []

        for param in params:
            name, typeStr = param
            paramType = Type.fromString(typeStr)
            paramsRecord[name] = paramType
            paramTypes.append(paramType)

        fnEnv = TypeEnvironment(paramsRecord, env)

        # Check the body in the extended environment:
        actualReturnType = self._tcBody(body, fnEnv)

        if not returnType.equals(actualReturnType):
            raise Exception(f"Expected function {body} to return {returnType}, but got {actualReturnType}")

        # Function type records its parameters and return type,
        # so we can use them to validate function calls:
        return Type.Function(None, paramTypes, returnType)

    # Checks a block.
    def _tcBlock(self, block, env):
        result = None
        _tag, *expressions = block

        for exp in expressions:
            result = self.tc(exp, env)

        return result

    # Creates a Global TypeEnvironment.
    def _createGlobal(self):
        return TypeEnvironment({
                'VERSION': Type.string,
                'sum': Type.fromString('Fn<number<number,number>>'),
                'square': Type.fromString('Fn<number<number>>'),
                'typeof': Type.fromString('Fn<string<any>>')
            }
        )

    # Boolean binary operators.
    def _booleanBinary(self, exp, env):
        self._checkArity(exp, 2)

        t1 = self.tc(exp[1], env)
        t2 = self.tc(exp[2], env)

        self._expect(t2, t1, exp[2], exp)

        return Type.boolean

    # Binary operators.
    def _binary(self, exp, env):
        self._checkArity(exp, 2)

        t1 = self.tc(exp[1], env)
        t2 = self.tc(exp[2], env)

        allowedTypes = self._getOperandTypesForOperator(exp[0])

        self._expectOperatorType(t1, allowedTypes, exp)
        self._expectOperatorType(t2, allowedTypes, exp)

        return self._expect(t2, t1, exp[2], exp)

    # Returns allowed operand types for an operator.
    def _getOperandTypesForOperator(self, operator):
        if operator == '+':
            return [Type.string, Type.number]
        elif operator == '-':
            return [Type.number]
        elif operator == '/':
            return [Type.number]
        elif operator == '*':
            return [Type.number]
        else:
            raise Exception(f"Unknown operator: {operator}.")

    # Throws if operator type doesn't expect the operand.
    def _expectOperatorType(self, type, allowedTypes, exp):
        # For union type, _all_ sub-types should support this operation:
        if isinstance(type, Type.Union):
            if type.includesAll(allowedTypes):
                return
        else:
            for allowedType in allowedTypes:
                if allowedType.equals(type):
                    return
        raise Exception(f"Unexpected type: {type} in {exp}, allowed: {allowedTypes}")


    # Expects a type.
    def _expect(self, actualType, expectedType, value, exp):
        if not actualType.equals(expectedType):
            self._throw(actualType, expectedType, value, exp)
        return actualType

    # Throws type error.
    def _throw(self, actualType, expectedType, value, exp):
        raise Exception(f"Expected: '{expectedType}' type for {value} in {exp}, but got '{actualType}' type.")

    # Throws for number of arguments.
    def _checkArity(self, exp, arity):
        if len(exp) - 1 != arity:
            raise Exception(f"Operator '{exp[0]}' expects {arity} operands, {len(exp)-1} given in {exp}.")

# Whether expression is a number.
def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

# Whether expression is a string.
def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')

# Whether the expression is a binary.
def isBinary(exp):
    return (type(exp[0]) == str) and re.search(r'^[+\-*/]$', exp[0])

# Whether expression is a variable name.
def isVariableName(exp):
    return (type(exp) == str) and re.search(r'^[+\-*/<>=a-zA-Z0-9_:]+$', exp)

# Whether the expression is a boolean.
def isBoolean(exp):
    return isinstance(exp, bool) or exp == True or exp == False

# Whether the expression is boolean binary.
def isBooleanBinary(exp):
    return (
        exp[0] == '==' or
        exp[0] == '!=' or
        exp[0] == '>=' or
        exp[0] == '<=' or
        exp[0] == '>' or
        exp[0] == '<'
    )