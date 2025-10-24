import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''
  // Each function can be spawned as a process:
  (def handle (id)
    (begin
      (print id 1)
      (print id 2)))

   (handle "x") // x 1, x 2
   (handle "y") // y 1, y 2

  // Parallel execution:
  // x 1, y 1, x 2, y 2, ...

  (spawn handle "x")
  (spawn handle "y")
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
