import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''
  // Lists:
  (var data (list 1 2 3))
  (idx data 0) // 1
  (print data (idx data 0))

  // Records:
  (var z 3)
  (var point (rec (x 1) (y 2) z))
  (prop point x) // 1
  (print point (prop point x))
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
