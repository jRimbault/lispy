from unittest import TestCase

from lispy import repl

from . import capture


class ReplTester(TestCase):
    def setUp(self):
        self.repl = repl.LispyRepl()

    def tearDown(self):
        del self.repl

    def test_end_of_line(self):
        with capture(self.repl.default, "EOF") as res:
            self.assertTrue(res)

    def test_insert_value(self):
        with capture(self.repl.default, "(let a 1)") as res:
            self.assertEqual("", res)

    def test_retrieve_value(self):
        with capture(self.repl.interpreter, "a") as res:
            self.assertEqual("1\n", res)

    def test_value_not_defined(self):
        with capture(self.repl.interpreter, "b") as res:
            self.assertEqual("Symbol 'b' not defined.\n", res)
