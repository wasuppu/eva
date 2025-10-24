# Type class.
class Type:

    def __init__(self, name):
        self.name = name

    # Return name.
    def getName(self):
        return self.name

    # String representation.
    def __repr__(self):
        return self.getName()

    # Equals.
    def equals(self, other):
        return self.name == other.name

def fromString(typeStr):
    if typeStr == 'number':
        return number
    elif typeStr == 'string':
        return string

    raise Exception(f"Unknown type: {typeStr}")

# Number type.
number = Type('number')

# String type.
string = Type('string')

