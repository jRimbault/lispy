"""Default Scheme env

An environment with some Scheme standard procedures.
"""
import math
import operator
import os

from .ltypes import Number, Symbol

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
        "not": operator.not_,
        "null?": lambda x: x == [],
        "number?": lambda x: isinstance(x, Number),
        "procedure?": callable,
        "round": round,
        "range": range,
        "symbol?": lambda x: isinstance(x, Symbol),
        "print": print,
        "display": print,
        "newline": os.linesep,
    }
)
