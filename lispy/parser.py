"""Parser module

Functions to tokenize a stream of characters.
"""

import io
import re

from . import ltypes
from .lex import lexer
from .graph import printTreeGraph


def parse(source: str, args) -> ltypes.Exp:
    """Read lisp from a string."""
    exps = read_from_tokens(tokenize(source))
    if args.render is not None:
        printTreeGraph(exps, args)
    return exps


def tokenize(source: str) -> list:
    """Convert a string of characters into a list of tokens."""
    return [token.value for token in lexer.lex(source)]


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

    if token == ")":
        raise SyntaxError("unexpected )")

    return ltypes.atom(token)
