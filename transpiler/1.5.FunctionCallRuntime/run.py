import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''
    (var user-name "John")
    (print "user =" user-name)
    (set user-name "Alex")
    (print "user =" user-name)
    (print (Number "1"))
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
