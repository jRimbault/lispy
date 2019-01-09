"""Default Scheme env

An environment with some Scheme standard procedures.
"""
import functools
import math
import operator
import os
import sys

from . import ltypes


def scheme_to_str(exp):
    """Convert a Python object back into a Scheme-readable string."""
    if isinstance(exp, ltypes.List):
        return "(" + " ".join(map(scheme_to_str, exp)) + ")"
    return str(exp)


def compose_functions(f, g):
    return lambda x: f(g(x))


# Get all math functions in the global space
# sin, cos, sqrt, pi, ...
GLOBAL_ENV = vars(math)
GLOBAL_ENV.pop("__doc__", None)
GLOBAL_ENV.pop("__loader__", None)
GLOBAL_ENV.pop("__name__", None)
GLOBAL_ENV.pop("__package__", None)
GLOBAL_ENV.pop("__spec__", None)
GLOBAL_ENV.update(
    {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "=": operator.eq,
        "%": operator.mod,
        "expt": lambda a, b: a ** b,
        "abs": abs,
        "append": operator.add,
        "args": sys.argv[1:],
        "modulo": operator.mod,
        "apply": lambda proc, args: proc(*args),
        "do": lambda *x: x[-1],
        "begin": lambda *x: x[-1],
        "car": lambda x: x[0],
        "cdr": lambda x: x[1:],
        "cons": lambda x, y: [x] + y,
        "eq?": operator.is_,
        "equal?": operator.eq,
        "length": len,
        "list": lambda *x: list(x),
        "list?": lambda x: isinstance(x, list),
        "map": lambda *args: list(map(*args)),
        "max": max,
        "min": min,
        "int": int,
        "str": str,
        "not": operator.not_,
        "null?": lambda x: x == [],
        "number?": lambda x: isinstance(x, ltypes.Number),
        "procedure?": callable,
        "round": round,
        "range": range,
        "symbol?": lambda x: isinstance(x, ltypes.Symbol),
        "print": lambda x: print(scheme_to_str(x)),
        "display": print,
        "newline": os.linesep,
        "compose": compose_functions
    }
)
