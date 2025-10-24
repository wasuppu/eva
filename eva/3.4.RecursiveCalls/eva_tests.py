# Atom:
atomTests = [
    ('1', 1),
    ('1.1', 1.1),
    ('"Hello"', 'Hello'),
]

# Math:
mathTests = [
    ('(+ 1 5)', 6),
    ('(+ (+ 3 2) 5)', 10),
    ('(+ (* 3 2) 5)', 11),
]

# Variables:
variableTests = [
    ('(var x 10)', 10),
    ('x', 10),
    ('(var y 100)', 100),
    ('y', 100),
    ('VERSION', '0.1'),
    ('(var isUser true)', True),
    ('(var z (* 2 2))', 4),
    ('z', 4),
]

# Blocks:
blockTests = [
    ('''
    (begin
      (var x 10)
      (var y 20)
      (+ (* x y) 30))
    ''', 230),

    ('''
    (begin
      (var x 10)
      (begin
        (var x 20)
        x)
     x)
    ''', 10),

    ('''
    (begin
      (var value 10)
      (var result
        (begin
          (var x (+ value 10))
          x))
      result)
    ''', 20),

    ('''
    (begin
      (var data 10)
      (begin
        (set data 100))
      data)
    ''', 100),
]

# IF:
ifTests = [
    ('''
    (begin
      (var x 10)
      (var y 0)
      (if (> x 10)
          (set y 20)
          (set y 30))
      y)
    ''', 30),
]

# While:
whileTests = [
    ('''
    (begin
      (var counter 0)
      (var result 0)
      (while (< counter 10)
        (begin
          (set result (+ result 1))
          (set counter (+ counter 1))))
      result)
    ''', 10),
]

# Comparision:
compTests = [
    ('(> 1 5)', False),
    ('(< 1 5)', True),
    ('(>= 5 5)', True),
    ('(<= 5 5)', True),
    ('(= 5 5)', True),
]

# User-defined function:
funcTests = [
    ('''
    (begin
      (def square (x)
        (* x x))
      (square 2))
    ''', 4),

    ('''
    (begin
      (def calc (x y)
        (begin
          (var z 30)
          (+ (* x y) z)))
      (calc 10 20))
    ''', 230),

    ('''
    (begin
      (var value 100)
      (def calc (x y)
        (begin
          (var z (+ x y))
          (def inner (foo)
            (+ (+ foo z) value))
          inner))
      (var fn (calc 10 20))
      (fn 30)
     )
    ''', 160),
]

# Lambda:
lambdaTests = [
  ('''
  (begin
    (def onClick (callback)
      (begin
        (var x 10)
        (var y 20)
        (callback (+ x y))))
    (onClick (lambda (data) (* data 10))))
  ''', 300),

  ('((lambda (x) (* x x)) 2)', 4),

  ('''
  (begin
    (var square (lambda (x) (* x x)))
    (square 2))
  ''', 4)
]

# Recursive calls:
recursiveTests = [
  ('''
  (begin
    (def factorial (x)
      (if (= x 1)
          1
          (* x (factorial (- x 1)))))
    (factorial 5))
  ''', 120)
]

tests = [*atomTests, *mathTests, *variableTests, *blockTests, *ifTests, *whileTests,
        *compTests, *funcTests, *lambdaTests, *recursiveTests]