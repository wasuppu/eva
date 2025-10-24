from rdp import Parser

parser = Parser()

# program = '42'
# program = '"hello"'
# program = "'hello'"
# program = '  42  '
# program = '  "  42  "  '
# program = '''
# // Number:
# 42
# '''
program = '''
   /**
   * Documentation comment
   */
   "hello"
'''

ast = parser.parse(program)
print(ast)