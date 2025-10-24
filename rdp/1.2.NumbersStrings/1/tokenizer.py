# Tokenizer class.
# Lazily pulls a token from a stream.
class Tokenizer:
    # Initializes the string.
    def __init__(self, string):
        self._string = string
        self._cursor = 0

    # Whether we still have more tokens.
    def hasMoreTokens(self):
        return self._cursor < len(self._string)

    # Obtains next token.
    def getNextToken(self):
        if not self.hasMoreTokens():
            return None
        string = self._string[self._cursor:]

        # Numbers
        if string[0].isdigit():
            number = ''
            while self.hasMoreTokens() and string[self._cursor].isdigit():
                number += string[self._cursor]
                self._cursor += 1
            return {'type': 'NUMBER', 'value': number}