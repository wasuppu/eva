import re

# Tokenizer Spec.
Spec = [
    # Whitespace
    [r'^\s+', None],

    # Comments
    # Skip single-line comments
    [r'^\/\/.*', None],
    # Skip multi-line comments
    [r'^\/\*[\s\S]*?\*\/', None],

    # Symbols, delimiters
    [r'^;', ';'],
    [r'^\{', '{'],
    [r'^\}', '}'],
    [r'^\(', '('],
    [r'^\)', ')'],
    [r'^,', ','],

    # Keywords
    [r'^\blet\b', 'let'],
    [r'^\bif\b', 'if'],
    [r'^\belse\b', 'else'],
    [r'^\btrue\b', 'true'],
    [r'^\bfalse\b', 'false'],
    [r'^\bnull\b', 'null'],

    # Numbers
    [r'^\d+', 'NUMBER'],

    # Identifiers
    [r'^\w+', 'IDENTIFIER'],

    # Equality operators: ==, !=
    [r'^[=!]=', 'EQUALITY_OPERATOR'],

    # Assignment operators: =, +=, -=, *=, /=
    [r'^=', 'SIMPLE_ASSIGN'],
    [r'^[-+*\/]=', 'COMPLEX_ASSIGN'],

    # Math operator: +, -
    [r'^[-+]', 'ADDITIVE_OPERATOR'],
    [r'^[*\/]', 'MULTIPLICATIVE_OPERATOR'],

    # Relational operators: >, >=, <, <=
    [r'^[><]=?', 'RELATIONAL_OPERATOR'],

    # Logical operators: &&, ||
    [r'^&&', 'LOGICAL_AND'],
    [r'^\|\|', 'LOGICAL_OR'],

    # Strings
    # Double quote string
    [r'^"[^"]*"', 'STRING'],
    # Single quote string
    [r"^'[^']*'", 'STRING']
]

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

        for regexp, tokenType in Spec:
            tokenValue = self._match(regexp, string)

            # Couldn't match this rule, continue.
            if tokenValue == None:
                continue

            # Should skip token, e.g. whitespace.
            if tokenType == None:
                return self.getNextToken()

            return {'type': tokenType, 'value': tokenValue}

        raise Exception('Unexpected token: %s'%(string[0]))

    # Matches a token for a regular expression.
    def _match(self, regexp, string):
        matched = re.compile(regexp).match(string)
        if matched == None:
            return None
        self._cursor += len(matched.group(0))
        return matched.group(0)


