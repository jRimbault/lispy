"""Lisp types

This modules defines the basic types available in the
lispy interpreter.
"""

# A Lisp Symbol is implemented as a Python str
Symbol = str
# A Lisp Number is implemented as a Python int or float
Number = (int, float)
# A Lisp Atom is a Symbol or Number
Atom = (Symbol, Number)
# A Lisp List is implemented as a Python list
List = list
# A Lisp expression is an Atom or List
Exp = (Atom, List)


def atom(token: str) -> Atom:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)
