"""Read Eval Print Loop Module"""

import cmd
import sys

from .core import BUILTINS, evaluate_exp, scheme_to_str
from .env import GLOBAL_ENV
from .parser import parse


def read_eval_print_loop():
    repl = LispyRepl()
    try:
        sys.exit(repl.cmdloop())
    except KeyboardInterrupt:
        print("Bye!")
    return 0


class LispyRepl(cmd.Cmd):
    intro = "Welcome to the lispy interpreter"
    prompt = "(lispy) > "
    autocomplete = list(GLOBAL_ENV.keys()) + list(BUILTINS.keys())
    file = None

    def default(self, line):
        if self.eof(line):
            return True
        self.interpreter(line)

    def interpreter(self, line):
        """Evaluate s-expressions"""
        try:
            val = evaluate_exp(parse(line))
            if val is not None:
                print(scheme_to_str(val))
        except KeyError as error:
            print(f"Symbol {error} not defined.")
        except Exception as error:
            print(f"{type(error).__name__}: {error}")

    def eof(self, line):
        """Check to quit"""
        if line == "EOF":
            print("Bye!")
            return True
        return False

    def completedefault(self, text, *_):
        return [i for i in self.autocomplete if i.startswith(text)]
