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
        return self.resolve(name).record[name]

    # Return specific environment in which a variable is defined, or throws if a variable is not defined.
    def resolve(self, name):
        if name in self.record:
            return self

        if self.parent == None:
            raise Exception(f'Variable "{name}" is not defined.')

        return self.parent.resolve(name)
