"""Parser module

Functions to tokenize a stream of characters.
"""

import io
import re

from . import ltypes


def parse(source: str) -> ltypes.Exp:
    """Read lisp from a string."""
    return read_from_tokens(tokenize(source))


def tokenize(source: str) -> list:
    """Convert a string of characters into a list of tokens."""
    return list(Tokenizer(io.StringIO(source)).get_tokens())


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


class Tokenizer:
    tokenizer = r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)"""

    def __init__(self, file):
        self.file = file
        self.line = ""

    def next_token(self):
        while True:
            if self.line == "":
                self.line = self.file.readline()
            if self.line == "":
                return None
            token, self.line = re.match(Tokenizer.tokenizer, self.line).groups()
            if token != "" and not token.startswith(";"):
                return token

    def get_tokens(self):
        while True:
            token = self.next_token()
            if token is None:
                break
            yield token
