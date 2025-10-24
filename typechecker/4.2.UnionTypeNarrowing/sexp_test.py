from sexp import Sexp

sexp = Sexp()

def test(sexp, code, expected):
    assert sexp.parse(code) == expected

# Empty lists.
test(sexp, '()', [])
test(sexp, '( )', [])
test(sexp, '( ( ) )', [ [ ] ])

# Simple atoms.
test(sexp, '1', 1)
test(sexp, '+', '+')
test(sexp, 'foo', 'foo')

# Non-empty and nested lists.
test(sexp, '(+ 1 15)', ['+', 1, 15])

test(sexp, '(* (+ 1 15) (- 15 2))', ['*', ['+', 1, 15], ['-', 15, 2]])

test(sexp, '''
  (define (fact n)
    (if (= n 0)
      1
    /* multi-line
    ** comment
    */
      (* n (fact (- n 1))))) // single line comment
''',

  ['define', ['fact', 'n'],
    ['if', ['=', 'n', 0],
      1,
      ['*', 'n', ['fact', ['-', 'n', 1]]]]]
)

test(sexp,
  '(define foo "test")',
  ['define', 'foo', '"test"']
)

print('All tests passed!')