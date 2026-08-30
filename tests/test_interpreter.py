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

    def test_modulo_operator(self):
        # Modulo on integers
        out, _ = run("print(5 % 3)")
        self.assertEqual(out, "2\n")
        out, _ = run("print(10 % 4)")
        self.assertEqual(out, "2\n")
        out, _ = run("print(7 % 7)")
        self.assertEqual(out, "0\n")

    def test_integer_division_operator(self):
        # Integer (floor) division on integers
        out, _ = run("print(7 // 2)")
        self.assertEqual(out, "3\n")
        out, _ = run("print(10 // 3)")
        self.assertEqual(out, "3\n")
        out, _ = run("print(8 // 2)")
        self.assertEqual(out, "4\n")

    def test_modulo_in_conditional(self):
        # Classic FizzBuzz-style check: a number is even if `n % 2 == 0`
        src = (
            "for i in range(1, 7):\n"
            "    if i % 2 == 0:\n"
            "        print(i, 'even')\n"
            "    else:\n"
            "        print(i, 'odd')\n"
        )
        out, _ = run(src)
        self.assertEqual(
            out,
            "1 odd\n2 even\n3 odd\n4 even\n5 odd\n6 even\n",
        )

    def test_modulo_by_zero_raises(self):
        with self.assertRaises(RuntimeError):
            run("x = 5 % 0\n")

    def test_integer_division_by_zero_raises(self):
        with self.assertRaises(RuntimeError):
            run("x = 5 // 0\n")

    def test_logical_and_truthy(self):
        # `True and 1` should evaluate to 1
        out, _ = run("print(True and 1)")
        self.assertEqual(out, "1\n")
        # `False and 1` should short-circuit and return False
        out, _ = run("print(False and 1)")
        self.assertEqual(out, "False\n")

    def test_logical_or_short_circuit(self):
        # `True or 1` should short-circuit to True
        out, _ = run("print(True or 1)")
        self.assertEqual(out, "True\n")
        # `False or 2` should evaluate the right side
        out, _ = run("print(False or 2)")
        self.assertEqual(out, "2\n")

    def test_elif_chain_picks_correct_branch(self):
        src = (
            "x = 5\n"
            "if x > 10:\n"
            "    print('big')\n"
            "elif x > 3:\n"
            "    print('medium')\n"
            "else:\n"
            "    print('small')\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "medium\n")

    def test_elif_with_and(self):
        # Multi-condition elif using 'and' / 'or'
        src = (
            "x = 6\n"
            "if x > 100:\n"
            "    print('huge')\n"
            "elif x % 2 == 0 and x % 3 == 0:\n"
            "    print('div6')\n"
            "elif x % 2 == 0:\n"
            "    print('even')\n"
            "else:\n"
            "    print('odd')\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "div6\n")

    def test_augmented_assignment_plus_equal(self):
        out, _ = run("x = 5\nx += 3\nprint(x)")
        self.assertEqual(out, "8\n")

    def test_augmented_assignment_compound(self):
        # Use a sequence of augmented assignments to update a running value
        src = (
            "x = 10\n"
            "x -= 4\n"   # 6
            "x *= 3\n"   # 18
            "x //= 5\n"  # 3
            "x %= 4\n"   # 3
            "x += 1\n"   # 4
            "print(x)\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "4\n")

    def test_augmented_assignment_in_loop(self):
        # Use += to accumulate a sum
        src = (
            "total = 0\n"
            "for i in range(1, 6):\n"
            "    total += i\n"
            "print(total)\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "15\n")

    def test_unary_minus(self):
        out, _ = run("x = -5\nprint(x)")
        self.assertEqual(out, "-5\n")
        out, _ = run("print(-(-3))")
        self.assertEqual(out, "3\n")
        out, _ = run("print(-(2 + 3))")
        self.assertEqual(out, "-5\n")

    def test_not_operator(self):
        out, _ = run("print(not True)")
        self.assertEqual(out, "False\n")
        out, _ = run("print(not False)")
        self.assertEqual(out, "True\n")
        out, _ = run("print(not 0)")
        self.assertEqual(out, "True\n")
        out, _ = run("print(not 1)")
        self.assertEqual(out, "False\n")
        out, _ = run("print(not not True)")
        self.assertEqual(out, "True\n")

    def test_not_in_conditional(self):
        # `not` is useful for inverting a condition
        src = (
            "x = 0\n"
            "if not x:\n"
            "    print('zero is falsy')\n"
            "else:\n"
            "    print('nonzero is truthy')\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "zero is falsy\n")

    def test_string_subscript(self):
        out, _ = run('s = "hello"\nprint(s[0])\nprint(s[1])\nprint(s[4])')
        self.assertEqual(out, "h\ne\no\n")

    def test_string_negative_subscript(self):
        out, _ = run('s = "hello"\nprint(s[-1])\nprint(s[-2])')
        self.assertEqual(out, "o\nl\n")

    def test_string_slice_via_index_expression(self):
        # Concatenating a few characters using indexing
        out, _ = run('s = "hello"\nprint(s[0] + s[1] + s[2])')
        self.assertEqual(out, "hel\n")

    def test_subscript_out_of_range_raises(self):
        with self.assertRaises(IndexError):
            run('s = "hi"\nprint(s[5])')

    def test_list_literal_and_indexing(self):
        src = (
            "nums = [10, 20, 30]\n"
            "print(nums[0])\n"
            "print(nums[1])\n"
            "print(nums[2])\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "10\n20\n30\n")

    def test_list_iteration_with_for(self):
        src = (
            "for n in [1, 2, 3]:\n"
            "    print(n)\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "1\n2\n3\n")

    def test_list_with_expressions(self):
        src = (
            "print([1 + 2, 3 * 4, 10 - 5])\n"
        )
        out, _ = run(src)
        # The print function calls str() on its args. The built-in print
        # is the host Python's, so it calls repr on the list, which looks
        # like "[3, 12, 5]".
        self.assertEqual(out, "[3, 12, 5]\n")

    def test_empty_list_length(self):
        src = "print(len([]))"
        out, _ = run(src)
        self.assertEqual(out, "0\n")

    def test_list_sum_via_for(self):
        # Compute the sum of a list using a for loop
        src = (
            "total = 0\n"
            "for n in [1, 2, 3, 4, 5]:\n"
            "    total += n\n"
            "print(total)\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "15\n")

    def test_in_list(self):
        # `x in [1, 2, 3]` - membership test against a list
        src = (
            "print(1 in [1, 2, 3])\n"
            "print(4 in [1, 2, 3])\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "True\nFalse\n")

    def test_in_string_substring(self):
        # `s in t` - substring test against a string
        src = (
            "print('ell' in 'hello')\n"
            "print('xyz' in 'hello')\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "True\nFalse\n")

    def test_in_used_in_conditional(self):
        # `in` is most useful as a guard in an if
        src = (
            "fruits = ['apple', 'banana', 'cherry']\n"
            "if 'banana' in fruits:\n"
            "    print('yes')\n"
            "else:\n"
            "    print('no')\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "yes\n")

    def test_not_in_list(self):
        # `x not in [1, 2, 3]` is the opposite of `x in [1, 2, 3]`
        src = (
            "print(1 not in [1, 2, 3])\n"
            "print(4 not in [1, 2, 3])\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "False\nTrue\n")

    def test_not_in_substring(self):
        src = (
            "print('ell' not in 'hello')\n"
            "print('xyz' not in 'hello')\n"
        )
        out, _ = run(src)
        self.assertEqual(out, "False\nTrue\n")


if __name__ == "__main__":
    unittest.main()
