from rdp import Parser

parser = Parser()

# program = '42'
# program = '"hello"'
program = "'hello'"

ast = parser.parse(program)
print(ast)