import Type
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

        raise Exception(f"Unknown type for expression {exp}.")

# Whether expression is a number.
def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

# Whether expression is a string.
def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')