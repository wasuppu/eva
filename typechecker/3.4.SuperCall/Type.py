import re
import sys
from TypeEnvironment import TypeEnvironment

current_module = sys.modules[__name__]

# Type class.
class Type:
    def __init__(self, name):
        self.name = name
        self.env = None

    # Return name.
    def getName(self):
        return self.name

    # String representation.
    def __repr__(self):
        return self.getName()

    # Equals.
    def equals(self, other):
        if isinstance(other, Alias):
            return other.equals(self)
        return self.name == other.name

def fromString(typeStr):
    if typeStr in globals():
        return globals()[typeStr]
    # from string: 'Fn<number>' -> Type.Function
    elif 'Fn<' in typeStr:
        if hasattr(current_module, typeStr):
            return getattr(current_module, typeStr)

        # Function type with return and params:
        matched = re.search(r'^Fn<(\w+)<([a-z,\s]+)>>$', typeStr)
        if matched:
            returnTypeStr, paramsString = matched.groups()

            paramTypes = list(map(lambda param: fromString(param), paramsString.split(',')))

            fn = Function(typeStr, paramTypes, fromString(returnTypeStr))
            setattr(current_module, typeStr, fn)
            return fn

        # Function type with return type only:
        matched = re.search(r'^Fn<(\w+)>$', typeStr)
        if matched:
            returnTypeStr = matched.groups()

            fn = Function(typeStr, [], fromString(returnTypeStr))
            setattr(current_module, typeStr, fn)
            return fn

    raise Exception(f"Unknown type: {typeStr}")

# Number type.
number = Type('number')

# String type.
string = Type('string')

# Boolean type.
boolean = Type('boolean')

# Null type.
null = Type('null')

# Function type.
function = lambda typeStr: fromString(typeStr)

# Function meta type.
class Function(Type):
    def __init__(self, name, paramTypes, returnType):
        super().__init__(name)
        self.paramTypes = paramTypes
        self.returnType = returnType

    '''
        Returns name: Fn<returnType<p1, p2, ...>>

        Fn<number> - function which returns a number

        Fn<number<number,number>> - function which returns a number, and accepts two numbers
    '''
    def getName(self):
        if self.name == None:
            name = ['Fn<', self.returnType.getName()]
            # Params.
            if len(self.paramTypes) != 0:
                params = []
                for i in range(0, len(self.paramTypes)):
                    params.append(self.paramTypes[i].getName())
                name.append('<')
                name.append(','.join(params))
                name.append('>')
            name.append('>')

            # Calculated name:
            self.name = ''.join(name)
        return self.name

    # Equals.
    def equals(self, other):
        if len(self.paramTypes) != len(other.paramTypes):
            return False

        # Same params.
        for i in range(0, len(self.paramTypes)):
             if not self.paramTypes[i].equals(other.paramTypes[i]):
                return False

        # Return type.
        if not self.returnType.equals(other.returnType):
            return False

        return True

# Type alias: (type int number)
class Alias(Type):
    def __init__(self, name, parent):
        super().__init__(name)
        self.parent = parent

    # Equals
    def equals(self, other):
        if self.name == other.name:
            return True
        return self.parent.equals(other)

# Class type: (class ...)
# Creates a new TypeEnvironment
class Class(Type):
    def __init__(self, name, superClass = null):
        super().__init__(name)
        self.superClass = superClass
        parent = None
        if superClass != None:
            parent = superClass.env
        self.env = TypeEnvironment({}, parent)

    # Return field type.
    def getField(self, name):
        return self.env.lookup(name)

    # Equals.
    def equals(self, other):
        if self == other:
            return True

        # Aliases:
        if isinstance(other, Alias):
            return other.equals(self)

        # Super class:
        if self.superClass != null:
            return self.superClass.equals(other)

        # Anything else:
        return False




