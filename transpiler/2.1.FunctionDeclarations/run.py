import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''
    (def square (x) (* x x))
    (print (square 2)) // 4
    (def sum (a b)
      (begin
        (var c 30)
        (* c (+ a b))))
    (print (sum 10 20)) // 900
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
