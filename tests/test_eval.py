from lispy import core
from lispy import parser


def lispeval(expr):
    return core.evaluate_exp(parser.parse(expr))


def test_0():
    assert lispeval("(+ 2 2)") == 4


def test_1():
    assert lispeval("(+ (* 2 100) (* 1 10))") == 210


def test_2():
    assert lispeval("(if (> 6 5) (+ 1 1) (+ 2 2))") == 2


def test_3():
    assert lispeval("(if (< 6 5) (+ 1 1) (+ 2 2))") == 4


def test_4():
    assert lispeval("(define x 3)") == None


def test_5():
    assert lispeval("x") == 3


def test_6():
    assert lispeval("(+ x x)") == 6


def test_7():
    assert lispeval("((lambda (x) (+ x x)) 5)") == 10


def test_8():
    assert lispeval("(define twice (lambda (x) (* 2 x)))") == None


def test_9():
    assert lispeval("(twice 5)") == 10


def test_10():
    assert (
        lispeval("(define compose-custom (lambda (f g) (lambda (x) (f (g x)))))")
        == None
    )


def test_11():
    assert lispeval("((compose-custom list twice) 5)") == [10]


def test_12():
    assert lispeval("(define repeat (lambda (f) (compose-custom f f)))") == None


def test_13():
    assert lispeval("((repeat twice) 5)") == 20


def test_14():
    assert lispeval("((repeat (repeat twice)) 5)") == 80


def test_15():
    assert (
        lispeval("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))")
        == None
    )


def test_16():
    assert lispeval("(fact 3)") == 6


def test_17():
    assert (
        lispeval("(fact 50)")
        == 30414093201713378043612608166064768844377641568960512000000000000
    )


def test_18():
    assert lispeval("(define abs-custom (lambda (n) ((if (> n 0) + -) 0 n)))") == None


def test_19():
    assert lispeval("(list (abs-custom -3) (abs-custom 0) (abs-custom 3))") == [3, 0, 3]


def test_20():
    assert (
        lispeval(
            """(define combine (lambda (f)
    (lambda (x y)
      (if (null? x) (quote ())
          (f (list (car x) (car y))
             ((combine f) (cdr x) (cdr y)))))))"""
        )
        == None
    )


def test_21():
    assert lispeval("(define zip (combine cons))") == None


def test_22():
    assert lispeval("(zip (list 1 2 3 4) (list 5 6 7 8))") == [
        [1, 5],
        [2, 6],
        [3, 7],
        [4, 8],
    ]


def test_23():
    assert (
        lispeval(
            """(define riff-shuffle (lambda (deck) (begin
    (define take (lambda (n seq) (if (<= n 0) (quote ()) (cons (car seq) (take (- n 1) (cdr seq))))))
    (define drop (lambda (n seq) (if (<= n 0) seq (drop (- n 1) (cdr seq)))))
    (define mid (lambda (seq) (/ (length seq) 2)))
    ((combine append) (take (mid deck) deck) (drop (mid deck) deck)))))"""
        )
        == None
    )


def test_24():
    assert lispeval("(riff-shuffle (list 1 2 3 4 5 6 7 8))") == [1, 5, 2, 6, 3, 7, 4, 8]


def test_25():
    assert lispeval("((repeat riff-shuffle) (list 1 2 3 4 5 6 7 8))") == [
        1,
        3,
        5,
        7,
        2,
        4,
        6,
        8,
    ]


def test_26():
    assert lispeval(
        "(riff-shuffle (riff-shuffle (riff-shuffle (list 1 2 3 4 5 6 7 8))))"
    ) == [1, 2, 3, 4, 5, 6, 7, 8]

