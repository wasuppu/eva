import json
from EvaMPP import EvaMPP

eva = EvaMPP()

# ast, target = eva.compile('''
#     (var x 42)
#     (if (== x 42)
#       (begin
#         (set x 100)
#          (print "Universe"))
#       (begin (print "Unknown")))
# ''').values()
# ast, target = eva.compile('''
#     (var i 5)
#     (while (> i 0)
#       (begin
#       //  (print "i =" i)
#         (set i (-- i))))
# ''').values()
ast, target = eva.compile('''
    (for (var i 5) (> i 0) (-- i)
       (print "i =" i))
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
