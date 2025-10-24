import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''

  (var point (rec (x 1) (y 2)))

  // Pattern matching:
  (match point
    (rec (x 1) (y 2)) (print "full match")
    (rec (x 1) y) (print "x match, y is" y)
    1 (print "point is 1")
    _ (print  "no match"))

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
