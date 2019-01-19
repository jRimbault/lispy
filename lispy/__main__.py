"""Should you want to run this as a module"""

import argparse
import io
import sys

from .core import evaluate_exp
from .parser import parse
from .repl import read_eval_print_loop


def main(args):
    """Main entry point for the interpreter"""
    if len(sys.argv) < 2 and sys.stdin.isatty():
        sys.exit(read_eval_print_loop())
    eval_file(args.file)


def parse_args(argv=sys.argv[1:]):
    """Define known options"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    args, _ = parser.parse_known_args(argv)
    return args


def eval_file(filename):
    """Helper method to interpret a file"""

    def commented_line(line):
        if ";" in line:
            return line[0 : line.index(";")]
        if "#" in line:
            return line[0 : line.index("#")]
        return line

    with io.open(filename) as stream:
        program = "".join(map(commented_line, stream))
    evaluate_exp(parse(f"(begin {program})"))


if __name__ == "__main__":
    main(parse_args())
