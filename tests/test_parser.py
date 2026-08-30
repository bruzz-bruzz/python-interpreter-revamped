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

    def test_and_or_in_expression(self):
        # `a and b` and `a or b` should parse as BinaryExpression with KEYWORD type
        # and the actual keyword stored in operator_value
        program = parse("a and b")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.BinaryExpression)
        self.assertEqual(expr.operator_value, "and")

        program = parse("a or b")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.BinaryExpression)
        self.assertEqual(expr.operator_value, "or")

    def test_and_binds_tighter_than_or(self):
        # `a or b and c` should be `a or (b and c)` (and binds tighter)
        program = parse("a or b and c")
        stmt = program.statements[0]
        expr = stmt.expression
        # Top is 'or'
        self.assertEqual(expr.operator_value, "or")
        # Right is 'and'
        self.assertIsInstance(expr.right, ast.BinaryExpression)
        self.assertEqual(expr.right.operator_value, "and")

    def test_comparison_binds_tighter_than_and(self):
        # `a > 1 and b > 2` should be `(a > 1) and (b > 2)` (comparison tighter)
        program = parse("a > 1 and b > 2")
        stmt = program.statements[0]
        expr = stmt.expression
        # Top is 'and'
        self.assertEqual(expr.operator_value, "and")
        # Both sides are comparisons
        self.assertEqual(expr.left.operator.value, "GREATER")
        self.assertEqual(expr.right.operator.value, "GREATER")

    def test_elif_chains_parse_to_nested_if(self):
        # An if/elif/else chain should parse to nested IfStatements
        program = parse("if a:\n    x = 1\nelif b:\n    x = 2\nelse:\n    x = 3\n")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.IfStatement)
        # elif becomes a nested IfStatement in else_body
        self.assertIsNotNone(stmt.else_body)
        self.assertEqual(len(stmt.else_body), 1)
        self.assertIsInstance(stmt.else_body[0], ast.IfStatement)
        # else becomes the inner IfStatement's else_body
        self.assertIsNotNone(stmt.else_body[0].else_body)

    def test_augmented_assignment_desugars(self):
        # `x += 1` should parse to AssignmentExpression(target=Variable(x), value=BinaryExpression(x + 1))
        program = parse("x += 1")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.AssignmentExpression)
        self.assertIsInstance(expr.target, ast.Variable)
        self.assertEqual(expr.target.name, "x")
        self.assertIsInstance(expr.value, ast.BinaryExpression)
        self.assertEqual(expr.value.operator.value, "PLUS")

    def test_parenthesized_expression(self):
        # `(1 + 2) * 3` should be parseable and bind like normal
        program = parse("(1 + 2) * 3")
        stmt = program.statements[0]
        expr = stmt.expression
        # Top is the multiplication
        self.assertIsInstance(expr, ast.BinaryExpression)
        self.assertEqual(expr.operator.value, "MULTIPLY")
        # Left is a parenthesized binary expression
        self.assertIsInstance(expr.left, ast.BinaryExpression)
        self.assertEqual(expr.left.operator.value, "PLUS")

    def test_unary_minus(self):
        program = parse("-5")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.UnaryExpression)
        self.assertEqual(expr.operator.value, "MINUS")

    def test_not_operator(self):
        program = parse("not True")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.UnaryExpression)
        self.assertEqual(expr.operator_value, "not")
        self.assertIsInstance(expr.operand, ast.Boolean)

    def test_subscript_expression(self):
        # `s[0]` should parse as a SubscriptExpression
        program = parse("s[0]")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.SubscriptExpression)
        self.assertIsInstance(expr.target, ast.Variable)
        self.assertEqual(expr.target.name, "s")
        self.assertIsInstance(expr.index, ast.Integer)
        self.assertEqual(expr.index.value, 0)

    def test_list_literal(self):
        # `[1, 2, 3]` should parse as a ListLiteral with three Integer elements
        program = parse("[1, 2, 3]")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.ListLiteral)
        self.assertEqual(len(expr.elements), 3)
        self.assertEqual(expr.elements[0].value, 1)
        self.assertEqual(expr.elements[1].value, 2)
        self.assertEqual(expr.elements[2].value, 3)

    def test_empty_list_literal(self):
        program = parse("[]")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.ListLiteral)
        self.assertEqual(expr.elements, [])

    def test_list_with_expressions(self):
        # List elements can be arbitrary expressions
        program = parse("[1 + 2, 3 * 4]")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.ListLiteral)
        self.assertEqual(len(expr.elements), 2)

    def test_in_operator_parses(self):
        # `3 in [1, 2, 3]` should be a BinaryExpression with operator_value='in'
        program = parse("3 in [1, 2, 3]")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.BinaryExpression)
        self.assertEqual(expr.operator_value, "in")
        self.assertIsInstance(expr.left, ast.Integer)
        self.assertIsInstance(expr.right, ast.ListLiteral)

    def test_not_in_operator_parses(self):
        # `3 not in [1, 2, 3]` should be a BinaryExpression with operator_value='not in'
        program = parse("3 not in [1, 2, 3]")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.BinaryExpression)
        self.assertEqual(expr.operator_value, "not in")
        self.assertIsInstance(expr.left, ast.Integer)
        self.assertIsInstance(expr.right, ast.ListLiteral)

    def test_unary_not_still_works(self):
        # `not` should still parse as UnaryExpression when not followed by `in`
        program = parse("not True")
        stmt = program.statements[0]
        expr = stmt.expression
        self.assertIsInstance(expr, ast.UnaryExpression)
        self.assertEqual(expr.operator_value, "not")

    def test_break_parses(self):
        # `break` should parse as a BreakStatement
        program = parse("break")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.BreakStatement)

    def test_continue_parses(self):
        # `continue` should parse as a ContinueStatement
        program = parse("continue")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ContinueStatement)

    def test_break_in_for(self):
        # `break` inside a for-loop should still parse
        src = (
            "for i in range(5):\n"
            "    if i == 2:\n"
            "        break\n"
        )
        program = parse(src)
        for_stmt = program.statements[0]
        if_stmt = for_stmt.body[0]
        break_stmt = if_stmt.body[0]
        self.assertIsInstance(break_stmt, ast.BreakStatement)


if __name__ == "__main__":
    unittest.main()
