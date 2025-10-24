import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''
    (var x 32)
    (var z (== x 10))
    (var y (* 5 (+ x 10)))
    (or (> x 0) (< x 100))
    (not x)
    (print (- y))
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
