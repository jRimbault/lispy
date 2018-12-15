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


BUILTINS = {
    "quote": _quote,
    "if": _if,
    "let": _define,
    "define": _define,
    "lambda": _lambda,
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
