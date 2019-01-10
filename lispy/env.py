"""Default Scheme env

An environment with some Scheme standard procedures.
"""
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


# Get all math functions in the global space
# sin, cos, sqrt, pi, ...
GLOBAL_ENV = {
    key: function for key, function in vars(math).items() if not key.startswith("__")
}
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
        "compose": lambda f, g: lambda x: f(g(x)),
        "type": type,
    }
)
