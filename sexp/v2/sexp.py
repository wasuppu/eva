#  Recursive descent parser
#  Grammer:
#  Sexp : Atom
#       | List
#
#  List : '(' ListEntries ')'
#
#  ListEntries : Sexp ListEntries
#              | ε
#
#  Atom : SYMBOL
#       | STRING
#       | NUMBER

import re

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def toNumber(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

class Sexp:
    def parse(self, expression):
        self._expression = expression
        self._cursor = 0
        self._ast = []
        return self._parseExpression()

    def _parseExpression(self):
        self._ignore()
        if self._expression[self._cursor] == '(':
            return self._parseList()
        return self._parseAtom()

    def _parseList(self):
        self._ast.append([])
        self._expect('(')
        self._parseListEntries()
        self._expect(')')
        return self._ast[0]

    def _parseListEntries(self):
        self._ignore()

        if self._expression[self._cursor] == ')':
            return

        entry = self._parseExpression()
        if entry != '':
            if isinstance(entry, list):
                entry = self._ast.pop()
            self._ast[len(self._ast)-1].append(entry)

        return self._parseListEntries()

    def _expect(self, c):
        if self._expression[self._cursor] != c:
            raise Exception('Unexpected token: ' + self._expression[self._cursor] + ', expected: ' + c)
        self._cursor += 1

    def _parseAtom(self):
        terminator = r'\s+|\)'
        atom = ''

        while self._cursor < len(self._expression) and re.search(terminator, self._expression[self._cursor]) == None:
            atom += self._expression[self._cursor]
            self._cursor += 1

        if atom != '' and isNumber(atom):
            atom = toNumber(atom)
        return atom

    def _ignore(self):
        specs = [
            r'^\s+', # Whitespaces
            r'^\/\/.*', # Skip single-line comments
            r'^\/\*[\s\S]*?\*\/', # Skip multi-line comments
        ]
        while self._cursor < len(self._expression):
            matched = False
            for spec in specs:
                match = re.search(spec, self._expression[self._cursor:])
                if match != None:
                    matched = True
                    _, end = match.span()
                    self._cursor += end
            if not matched:
                break