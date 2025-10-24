import json
from EvaMPP import EvaMPP

eva = EvaMPP()

ast, target = eva.compile('''
  // Sending messages
  (def success (param)
    (print "Success =" param))

  (def not-found (url)
    (print "Not found:" url))

  (def handle-connection (data)
    (receive request
      "hello" (success 100)
      (rec (code 200) len)
        (begin
          (success len)
          (handle-connection data))
      (rec (code 404) url) (not-found url)
      _ (print data)))

  (var p1 (spawn handle-connection "default"))
  (var i 0)
  (def send-message ()
    (begin
      (set i (+ i 1))
      (if (<= i 5)
        (send p1 (rec (code 200) (len i)))
        (send p1 "hello"))
    )
  )
  (set-interval send-message 500)
  // (send p1 "hello")
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
