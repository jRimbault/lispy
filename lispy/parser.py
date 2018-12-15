"""Parser module

Functions to tokenize a stream of characters.
"""

from . import ltypes


def parse(source: str) -> ltypes.Exp:
    """Read lisp from a string."""
    return read_from_tokens(tokenize(source))


def tokenize(source: str) -> list:
    """Convert a string of characters into a list of tokens."""
    return source.replace("(", " ( ").replace(")", " ) ").split()


def read_from_tokens(tokenized_source: list) -> ltypes.Exp:
    """Read an expression from a sequence of tokens."""
    if not tokenized_source:
        raise SyntaxError("unexpected EOF")
    token = tokenized_source.pop(0)
    if token == "(":
        tokens = []
        while tokenized_source[0] != ")":
            tokens.append(read_from_tokens(tokenized_source))
        tokenized_source.pop(0)  # pop off ')'
        return tokens
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return ltypes.atom(token)
