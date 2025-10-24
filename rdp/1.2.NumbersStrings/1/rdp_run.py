from rdp import Parser

parser = Parser()

program = '42'
ast = parser.parse(program)
print(ast)