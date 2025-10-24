import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''
    42
    "hello"
''').values()

print('\n----------------------------')
print('1. Compiled AST:\n')

# JS AST:
print(json.dumps(ast, indent=2))

print('\n----------------------------')
print('2. Compiled code:\n')

# JS Code:
print(target)

print('\n----------------------------')
print('3. Result:\n')

# executed from ./compile-run.sh