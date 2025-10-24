# TypeEnvironment: mapping from names to types.
class TypeEnvironment:
    # Creates an environment with the given record.
    def __init__(self, record, parent):
        self.record = record
        self.parent = parent

    # Creates a variable with the given name and a type.
    def define(self, name, type):
        self.record[name] = type
        return type

    # Return the type of a defined variable, or throws if the variable is not defined.
    def lookup(self, name):
        if not name in self.record:
            raise Exception(f'Variable "{name}" is not defined.')
        return self.record[name]


