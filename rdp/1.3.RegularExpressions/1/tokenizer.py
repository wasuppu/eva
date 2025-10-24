import re

# Tokenizer class.
# Lazily pulls a token from a stream.
class Tokenizer:
    # Initializes the string.
    def __init__(self, string):
        self._string = string
        self._cursor = 0

    # Whether the tokenizer reached EOF.
    def isEOF(self):
        return self._cursor == len(self._string)

    # Whether we still have more tokens.
    def hasMoreTokens(self):
        return self._cursor < len(self._string)

    # Obtains next token.
    def getNextToken(self):
        if not self.hasMoreTokens():
            return None
        string = self._string[self._cursor:]

        # Numbers \d+
        matched = re.compile(r'^\d+').match(string)
        if matched != None:
            self._cursor += len(matched.group(0))
            return {'type': 'NUMBER', 'value': matched.group(0)}

        # String:
        matched = re.compile(r'^"[^"]*"').match(string)
        if matched != None:
            self._cursor += len(matched.group(0))
            return {'type': 'STRING', 'value': matched.group(0)}

        matched = re.compile(r"^'[^']*'").match(string)
        if matched != None:
            self._cursor += len(matched.group(0))
            return {'type': 'STRING', 'value': matched.group(0)}
