# Environment: names storage.
class Environment:
    # Creates an environment with the given record.
    def __init__(self, record = None, parent = None):
        self.record = record or dict()
        self.parent = parent

    # Creates a variable with the given name and value.
    def define(self, name, value):
        self.record[name] = value
        return value

    # Returns the value of a define variable, or throws if the variable is not defined.
    def lookup(self, name):
        return self.resolve(name).record[name]

    # Returns specific environment in which a variable is defined, or throws if a variable is not defined.
    def resolve(self, name):
        if name in self.record:
            return self

        if self.parent == None:
            raise Exception(f'Variable: "{name}" is not defined.')

        return self.parent.resolve(name)
