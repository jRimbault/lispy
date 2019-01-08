"""Lispy core

Interpreter main methods
"""

from collections import ChainMap as Environment

from . import ltypes
from .env import GLOBAL_ENV


def scheme_to_str(exp):
    """Convert a Python object back into a Scheme-readable string."""
    if isinstance(exp, ltypes.List):
        return "(" + " ".join(map(scheme_to_str, exp)) + ")"
    return str(exp)


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
    if var in env:
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
    if name_proc in env:
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


BUILTINS = {
    "quote": _quote,
    "if": _if,
    "let": _define,
    "define": _define,
    "lambda": _lambda,
    "defun": _defun,
    "cond": _cond,
    "λ": _lambda,
}


def evaluate_exp(expr: ltypes.Exp, env=GLOBAL_ENV) -> ltypes.Exp:
    """Evaluate an expression in an environment."""

    if isinstance(expr, ltypes.Symbol):  # variable reference
        return env[expr]
    if not isinstance(expr, ltypes.List):  # constant literal
        return expr

    try:
        return BUILTINS[expr[0]](expr, env)
    except KeyError:
        # (proc arg...)
        proc = evaluate_exp(expr[0], env)
        args = [evaluate_exp(exp, env) for exp in expr[1:]]
        return proc(*args)
    except TypeError as error:
        if "unhashable type: 'list'" in repr(error):
            # (proc arg...)
            proc = evaluate_exp(expr[0], env)
            args = [evaluate_exp(exp, env) for exp in expr[1:]]
            return proc(*args)
        raise


class Procedure(object):
    """A user-defined Scheme procedure."""

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        try:
            env = Environment(dict(zip(self.params, args)), self.env)
            # env = dict(zip(self.params, args))
            # env.update(self.env)
            return evaluate_exp(self.body, env)
        except TypeError as error:
            print(error)
            return None
