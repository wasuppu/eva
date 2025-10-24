# Eva interpreter.
class Eva:
    def eval(self, exp):

        if isNumber(exp):
            return exp

        if isString(exp):
            return exp[1:-1]

        if exp[0] == '+':
            return exp[1] + exp[2]

        raise Exception("Unimplemented: " + str(exp))


def isNumber(exp):
    return (type(exp) == int) or (type(exp) == float)

def isString(exp):
    return (type(exp) == str) and (exp[0] == '"') and (exp[-1] == '"')

# Test:
eva = Eva()

assert eva.eval(1) == 1
assert eva.eval('"Hello"') == "Hello"

assert eva.eval(['+', 1, 5]) == 6

print("All assertions passed!")


