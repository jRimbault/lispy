"""Lispy core

Interpreter main methods
"""

from collections import ChainMap as Environment
from functools import partial

from . import ltypes
from .env import GLOBAL_ENV


def _quote(expr, env):
    """(quote expr)"""
    (_, exp) = expr
    return exp


def _if(expr, env):
    """(if test conseq alt)"""
    (_, test, conseq, alt) = expr
    exp = conseq if evaluate_exp(test, env) else alt
    return evaluate_exp(exp, env)


def _define(expr, env):
    """(define var exp)"""
    (_, var, exp) = expr
    if var in env or var in BUILTINS:
        raise SyntaxError(f"Symbol '{var}' is already defined.")
    env[var] = evaluate_exp(exp, env)
    return None


def _lambda(expr, env):
    """(lambda (var...) body)"""
    (_, params, body) = expr
    return Procedure(params, body, env)


def _defun(expr, env):
    """(defun proc (arg) (exp))"""
    (_, name_proc, params, body) = expr
    if name_proc in env or name_proc in BUILTINS:
        raise SyntaxError(f"Symbol '{name_proc}' is already defined.")
    env[name_proc] = Procedure(params, body, env)
    return None


def _cond(expr, env):
    """(cond ((expr)...) (else expr))"""
    to_eval = expr[-1][1]
    for e in expr[1:-1]:
        if evaluate_exp(e[0], env) == True:
            to_eval = e[1:]
            if len(e[1:]) == 1:
                to_eval = e[1]
            break

    return evaluate_exp(to_eval, env)


def _loop(expr, env):
    """(loop for x from a to b do (proc))"""
    _, _, var, _, init, _, end, _, proc = expr
    if var in env or var in BUILTINS:
        raise SyntaxError(f"Symbol '{var}' is already defined outside the loop.")
    for i in range(init, end):
        env[var] = i
        evaluate_exp(proc, env)
    del env[var]


BUILTINS = {
    "quote": _quote,
    "if": _if,
    "let": _define,
    "define": _define,
    "lambda": _lambda,
    "defun": _defun,
    "cond": _cond,
    "loop": _loop,
    "λ": _lambda,
}


def evaluate_exp(expr: ltypes.Exp, env=GLOBAL_ENV) -> ltypes.Exp:
    """Evaluate an expression in an environment."""

    def _eval(expr, env):
        # (proc arg...)
        proc = evaluate_exp(expr[0], env)
        args = [evaluate_exp(exp, env) for exp in expr[1:]]
        return proc(*args)

    if isinstance(expr, ltypes.Symbol):  # variable reference
        return env[expr]
    if not isinstance(expr, ltypes.List):  # constant literal
        return expr

    try:
        return BUILTINS[expr[0]](expr, env)
    except KeyError:
        return _eval(expr, env)
    except TypeError as error:
        if "unhashable type: 'list'" in repr(error):
            return _eval(expr, env)


class Procedure(object):
    """A user-defined Scheme procedure."""

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        env = Environment(dict(zip(self.params, args)), self.env)
        return evaluate_exp(self.body, env)
