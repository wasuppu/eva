# Eva interpreter.
class Eva:
    def eval(self, exp):

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

        raise Exception("Unimplemented: " + str(exp))


def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')

# Test:
eva = Eva()

assert eva.eval(1) == 1
assert eva.eval('"Hello"') == "Hello"

# Math:
assert eva.eval(['+', 1, 5]) == 6
assert eva.eval(['+', ['+', 3, 2], 5]) == 10
assert eva.eval(['+', ['*', 3, 2], 5]) == 11

print("All assertions passed!")


