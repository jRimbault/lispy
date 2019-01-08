from unittest import TestCase

from lispy import core, parser, main, parse_args

from . import capture, HERE


class InterpreterTester(TestCase):
    def setUp(self):
        self.program = "(begin (define r 10) (* pi (* r r)))"
        self.tokens = ["(", "begin", "(", "define", "r", "10", ")", "(", "*", "pi", "(", "*", "r", "r", ")", ")", ")"]
        self.lisp = ["begin", ["define", "r", 10], ["*", "pi", ["*", "r", "r"]]]
        self.res = 314.1592653589793

    def tearDown(self):
        del self.program
        del self.tokens
        del self.lisp
        del self.res

    def test_tokenizer(self):
        self.assertEqual(self.tokens, parser.tokenize(self.program))

    def test_parse(self):
        self.assertEqual(self.lisp, parser.parse(self.program))

    def test_eval(self):
        self.assertEqual(self.res, core.evaluate_exp(self.lisp))


class FileInterpreterTester(TestCase):
    def setUp(self):
        self.args = [
            HERE + "/fibonacci.scm"
        ]
        self.res = "[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]"

    def tearDown(self):
        del self.args
        del self.res

    def test_interpret_file(self):
        with capture(main, parse_args(self.args)) as output:
            self.assertEqual(self.res, output.strip())
