# Typed Eva: static typecheker.
class EvaTC:

    # Infers and validates type of an expression.
    def tc(self, exp):
    # Self-evaluating:

        # Numbers
        if isNumber(exp):
            return 'number'

        raise Exception(f"Unknown type for expression {exp}.")


# Whether expression is a number.
def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)