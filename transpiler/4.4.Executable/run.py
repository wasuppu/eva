import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''

(def handle-process (el)
  (while (< (get-width el) RACE_LENGTH)
    (receive request
      (rec sender delay delta)
      (begin

        (inc-width el delta)
        (var receiver (get-random-process))

        (send receiver
          (rec
            (sender self)
            (delay (random 50 200))
            (delta (random 5 50))))

        (sleep delay)
      )
    )
  )
)

''', './out.js').values()

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
