from lispy import core, parser

from . import capture


def lispeval(expr):
    return core.evaluate_exp(parser.parse(expr))


def test_list_definition():
    expr = "(list 1 2 3 4)"
    assert lispeval(expr) == [1, 2, 3, 4]


def test_addition():
    expr = "(+ 1 1)"
    assert lispeval(expr) == 2


def test_multiplication():
    expr = "(* 2.24 3)"
    assert 0 < lispeval(expr) - 6.72 < 0.00001


def test_parser_syntax():
    expr = ")(let a 1)"
    error_happened = False
    try:
        lispeval(expr)
    except Exception as err:
        error_happened = True
        assert type(err) == SyntaxError
    assert error_happened == True


def test_type_error():
    expr = "(+ 1 (quote word))"
    error_happened = False
    try:
        lispeval(expr)
    except Exception as err:
        error_happened = True
        assert type(err) == TypeError
    assert error_happened == True


def test_procedure_definition():
    expr = "(lambda (x) (+ x 1))"
    assert type(lispeval(expr)) == core.Procedure


def test_lambda_application():
    expr = "((lambda (x) (+ x 1)) 1)"
    assert lispeval(expr) == 2


def test_lambda2_application():
    expr = "((lambda (x y) (+ x y)) 1 2)"
    assert lispeval(expr) == 3


def test_lambda3_application():
    expr = """((lambda (x y) (+ x y))
                (list 1 2)
                (list 3 4))"""
    assert lispeval(expr) == [1, 2, 3, 4]


def test_map_lambda_application():
    expr = """(map
                (lambda (x) (* x x))
                (list 1 2 3 4))"""
    assert lispeval(expr) == [1, 4, 9, 16]


def test_conditional_equals():
    expr = "(= 2 2)"
    assert lispeval(expr) == True


def test_conditional_lessthan():
    expr = "(< 1 2)"
    assert lispeval(expr) == True


def test_conditional_if():
    expr = "(if (= 2 2) 0 10)"
    assert lispeval(expr) == 0


def test_scopes_do_not_overlap():
    lispeval("(let var 10)")
    lispeval("(let identity (lambda (var) var))")
    error_happened = False
    try:
        lispeval("(let var 11)")
    except Exception as err:
        error_happened = True
        assert type(err) == SyntaxError
    assert error_happened == True
    assert lispeval("(identity 2)") == 2


def test_defun_proc():
    lispeval("(defun addition (x y) (+ x y))")
    assert lispeval("(addition 2 3)") == 5
    error_happened = False
    try:
        lispeval("(defun addition (x) x)")
    except Exception as err:
        error_happened = True
        assert type(err) == SyntaxError
    assert error_happened == True


def test_cond1_builtin():
    expr = """(cond ((= 1 1) 10)
                    ((= 2 1) (+ 20 1))
                    (else    30))"""
    assert lispeval(expr) == 10


def test_cond2_builtin():
    expr = """(cond ((= 1 2) 10)
                    ((= 2 2) (+ 20 1))
                    (else    30))"""
    assert lispeval(expr) == 21


def test_cond3_builtin():
    expr = """(cond ((= 1 2) 10)
                    ((= 2 1) (+ 20 1))
                    (else    30))"""
    assert lispeval(expr) == 30


def test_loop1_builtin():
    expr = "(loop for i from 0 to 10 do (print i))"
    with capture(lispeval, expr) as out:
        assert out.strip() == "\n".join(map(str, range(0, 10)))


def test_loop2_builtin_exception():
    lispeval("(let i 0)")
    error_happened = False
    try:
        lispeval("(loop for i from 0 to 10 do (print i))")
    except Exception as err:
        error_happened = True
        assert type(err) == SyntaxError
    assert error_happened == True


def test_forbid_redefinition_of_builtins():
    expr = "(let if 1)"
    error_happened = False
    try:
        lispeval(expr)
    except Exception as err:
        error_happened = True
        assert type(err) == SyntaxError
    assert error_happened == True


def test_exception_handling():
    lispeval("(let a-list (list 1))")
    error = lispeval("(try (car (cdr a-list)) error)")
    assert type(error) == IndexError
