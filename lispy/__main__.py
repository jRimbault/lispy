"""Should you want to run this as a module"""

import argparse
import io
import sys

from .core import evaluate_exp
from .parser import parse
from .repl import read_eval_print_loop


def main(args):
    if len(sys.argv) < 2 and sys.stdin.isatty():
        sys.exit(read_eval_print_loop())
    eval_file(args.file)


def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    return parser.parse_args(argv)


def eval_file(filename):
    def commented_line(line):
        if line.startswith(";") or line.startswith("#!"):
            return False
        if len(line) > 1:
            return True
        return False

    with io.open(filename) as stream:
        program = "".join(filter(commented_line, stream))
    evaluate_exp(parse(f"(begin {program})"))


if __name__ == "__main__":
    main(parse_args())
