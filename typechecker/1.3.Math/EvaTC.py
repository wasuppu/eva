import Type
import re

# Typed Eva: static typecheker.
class EvaTC:

    # Infers and validates type of an expression.
    def tc(self, exp):
    # Self-evaluating:

        # Numbers
        if isNumber(exp):
            return Type.number

        # Strings
        if isString(exp):
            return Type.string

        # Math operations:
        if isBinary(exp):
            return self._binary(exp)

        raise Exception(f"Unknown type for expression {exp}.")

    # Binary operators.
    def _binary(self, exp):
        self._checkArity(exp, 2)

        t1 = self.tc(exp[1])
        t2 = self.tc(exp[2])

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
        exist = False
        for allowedType in allowedTypes:
            if allowedType.equals(type):
                exist = True
                break
        if not exist:
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
    return re.search(r'^[+\-*/]$', exp[0])