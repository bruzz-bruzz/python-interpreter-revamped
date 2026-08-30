"""Smoke tests for the parser (run with `python -m unittest tests.test_parser`)."""

import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.ast import nodes as ast
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def parse(src):
    return Parser(Lexer(src).tokenize()).parse()


class ParserTests(unittest.TestCase):
    def test_empty_program(self):
        program = parse("")
        self.assertIsInstance(program, ast.Program)
        self.assertEqual(program.statements, [])

    def test_integer_assignment(self):
        program = parse("x = 42")
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ExpressionStatement)
        self.assertIsInstance(stmt.expression, ast.AssignmentExpression)
        self.assertIsInstance(stmt.expression.target, ast.Variable)
        self.assertEqual(stmt.expression.target.name, "x")

    def test_arithmetic_expression(self):
        program = parse("y = 1 + 2 * 3")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ExpressionStatement)
        assign = stmt.expression
        self.assertIsInstance(assign, ast.AssignmentExpression)
        self.assertIsInstance(assign.value, ast.BinaryExpression)
        # Multiplication binds tighter -> top op is '+'
        self.assertEqual(assign.value.operator.value, "PLUS")

    def test_function_definition(self):
        program = parse("def foo(a, b):\n    return a + b\n")
        self.assertEqual(len(program.statements), 1)
        func = program.statements[0]
        self.assertIsInstance(func, ast.FunctionDefinition)
        self.assertEqual(func.name, "foo")
        self.assertEqual(func.parameters, ["a", "b"])
        self.assertEqual(len(func.body), 1)
        self.assertIsInstance(func.body[0], ast.ReturnStatement)

    def test_if_statement(self):
        program = parse("if x > 0:\n    y = 1\n")
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.IfStatement)

    def test_while_loop(self):
        program = parse("while i < 10:\n    i = i + 1\n")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.WhileStatement)

    def test_for_loop(self):
        program = parse("for i in range(3):\n    print(i)\n")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ForStatement)
        self.assertEqual(stmt.target, "i")
        self.assertIsInstance(stmt.iterable, ast.FunctionCall)

    def test_function_call_parsing(self):
        program = parse("print(add(1, 2))")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ExpressionStatement)
        outer = stmt.expression
        self.assertIsInstance(outer, ast.FunctionCall)
        self.assertEqual(outer.function.name, "print")
        self.assertEqual(len(outer.arguments), 1)
        inner = outer.arguments[0]
        self.assertIsInstance(inner, ast.FunctionCall)
        self.assertEqual(inner.function.name, "add")

    def test_modulo_expression(self):
        # `5 % 3` should parse as a single BinaryExpression with MODULO operator
        program = parse("5 % 3")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ExpressionStatement)
        expr = stmt.expression
        self.assertIsInstance(expr, ast.BinaryExpression)
        self.assertEqual(expr.operator.value, "MODULO")
        self.assertIsInstance(expr.left, ast.Integer)
        self.assertEqual(expr.left.value, 5)
        self.assertIsInstance(expr.right, ast.Integer)
        self.assertEqual(expr.right.value, 3)

    def test_integer_division_expression(self):
        # `7 // 2` should parse as a single BinaryExpression with INTEGER_DIVIDE operator
        program = parse("7 // 2")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ExpressionStatement)
        expr = stmt.expression
        self.assertIsInstance(expr, ast.BinaryExpression)
        self.assertEqual(expr.operator.value, "INTEGER_DIVIDE")
        self.assertEqual(expr.left.value, 7)
        self.assertEqual(expr.right.value, 2)

    def test_modulo_precedence_tighter_than_addition(self):
        # `1 + 5 % 3` should be parsed as `1 + (5 % 3)` (modulo binds tighter)
        program = parse("1 + 5 % 3")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.BinaryExpression)
        # Top-level is PLUS
        self.assertEqual(expr.operator.value, "PLUS")
        # Right child is the MODULO
        self.assertIsInstance(expr.right, ast.BinaryExpression)
        self.assertEqual(expr.right.operator.value, "MODULO")


if __name__ == "__main__":
    unittest.main()
