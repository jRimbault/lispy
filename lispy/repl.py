"""Read Eval Print Loop Module"""

import cmd

from .core import BUILTINS, evaluate_exp
from .env import GLOBAL_ENV, scheme_to_str
from .parser import parse


def read_eval_print_loop():
    """Starts the repl"""
    repl = LispyRepl()
    try:
        repl.cmdloop()
    except KeyboardInterrupt:
        print("Bye!")
    return 0


class LispyRepl(cmd.Cmd):
    """Implements the cmd.Cmd std module to provide a repl"""

    intro = "Welcome to the lispy interpreter (tab completion enabled)"
    prompt = "(lispy) > "
    autocomplete = list(GLOBAL_ENV.keys()) + list(BUILTINS.keys())
    file = None

    def default(self, line):
        """Default method to implement"""
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
        """Tab autocomplete feature"""
        return [i for i in self.autocomplete if i.startswith(text)]
