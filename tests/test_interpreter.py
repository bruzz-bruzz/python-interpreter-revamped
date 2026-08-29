"""End-to-end tests for the interpreter (run with `python -m unittest tests.test_interpreter`)."""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.interpreter.interpreter import Interpreter
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def run(src):
    tokens = Lexer(src).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    buf = io.StringIO()
    with redirect_stdout(buf):
        interp.interpret(program)
    return buf.getvalue(), interp


class InterpreterTests(unittest.TestCase):
    def test_arithmetic_and_print(self):
        out, _ = run("print(1 + 2 * 3)")
        self.assertEqual(out, "7\n")

    def test_variable_assignment_visible_after(self):
        out, _ = run("x = 5\nprint(x)")
        self.assertEqual(out, "5\n")

    def test_function_returns_value(self):
        src = "def add(a, b):\n    return a + b\nprint(add(3, 4))\n"
        out, _ = run(src)
        self.assertEqual(out, "7\n")

    def test_recursive_factorial(self):
        src = (
            "def fact(n):\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return n * fact(n - 1)\n"
            "print(fact(5))\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "120\n")

    def test_while_loop_sum(self):
        src = (
            "total = 0\n"
            "i = 1\n"
            "while i <= 5:\n"
            "    total = total + i\n"
            "    i = i + 1\n"
            "print(total)\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "15\n")

    def test_for_loop_with_range(self):
        src = "for i in range(3):\n    print(i)\n"
        out, _ = run(src)
        self.assertEqual(out, "0\n1\n2\n")

    def test_comparison_in_if(self):
        src = (
            "x = 10\n"
            "if x > 5:\n"
            "    print(\"big\")\n"
            "else:\n"
            "    print(\"small\")\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "big\n")

    def test_undefined_variable_raises(self):
        with self.assertRaises(NameError):
            run("print(does_not_exist)")

    def test_division_by_zero_raises(self):
        with self.assertRaises(RuntimeError):
            run("x = 1 / 0\n")


if __name__ == "__main__":
    unittest.main()
