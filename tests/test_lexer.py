"""Smoke tests for the lexer (run with `python -m unittest tests.test_lexer`)."""

import os
import sys
import unittest

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.lexer.lexer import Lexer, TokenType


def lex(src):
    return Lexer(src).tokenize()


class LexerTests(unittest.TestCase):
    def test_integer_literal(self):
        tokens = lex("42")
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[0].value, 42)

    def test_float_literal(self):
        tokens = lex("3.14")
        self.assertEqual(tokens[0].type, TokenType.FLOAT)
        self.assertEqual(tokens[0].value, 3.14)

    def test_string_literal(self):
        tokens = lex('"hello"')
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello")

    def test_identifier_and_keyword(self):
        tokens = lex("foo def")
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.KEYWORD)

    def test_assignment_operator(self):
        tokens = lex("x = 1")
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.EQUAL)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(tokens[2].type, TokenType.INTEGER)

    def test_double_char_operators_come_first(self):
        # `==` must be tokenized as a single EQUAL_EQUAL, not two '='
        tokens = lex("a == b")
        self.assertEqual(tokens[1].type, TokenType.EQUAL_EQUAL)
        self.assertEqual(tokens[1].value, "==")

    def test_indent_dedent_emitted(self):
        tokens = lex("if True:\n    x = 1\n")
        types = [t.type for t in tokens]
        self.assertIn(TokenType.INDENT, types)
        self.assertIn(TokenType.DEDENT, types)

    def test_comments_are_skipped(self):
        tokens = lex("# this is a comment\nx = 1\n")
        for t in tokens:
            self.assertNotEqual(t.type, TokenType.COMMENT)
        self.assertTrue(
            any(t.type == TokenType.IDENTIFIER and t.value == "x" for t in tokens)
        )

    def test_modulo_operator(self):
        # `%` is a single MODULO token
        tokens = lex("5 % 3")
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[1].type, TokenType.MODULO)
        self.assertEqual(tokens[1].value, "%")
        self.assertEqual(tokens[2].type, TokenType.INTEGER)

    def test_integer_division_operator(self):
        # `//` must be tokenized as a single INTEGER_DIVIDE (not two DIVIDEs)
        tokens = lex("7 // 2")
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[1].type, TokenType.INTEGER_DIVIDE)
        self.assertEqual(tokens[1].value, "//")
        self.assertEqual(tokens[2].type, TokenType.INTEGER)
        # No stray DIVIDE tokens
        self.assertNotIn(TokenType.DIVIDE, [t.type for t in tokens])

    def test_divide_and_modulo_distinct(self):
        # `/` and `//` and `%` should all be distinct tokens
        tokens = lex("/ // %")
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        self.assertEqual(
            types, [TokenType.DIVIDE, TokenType.INTEGER_DIVIDE, TokenType.MODULO]
        )

    def test_augmented_assignment_operators(self):
        # `+=`, `-=`, `*=`, `/=`, `//=`, `%=` should each be single tokens,
        # not a single-char operator followed by `=`.
        for src, expected_type in [
            ("x += 1", TokenType.PLUSEQUAL),
            ("x -= 1", TokenType.MINUSEQUAL),
            ("x *= 1", TokenType.MULTIPLYEQUAL),
            ("x /= 1", TokenType.DIVIDEEQUAL),
            ("x //= 1", TokenType.INTEGERDIVIDEEQUAL),
            ("x %= 1", TokenType.MODULOEQUAL),
        ]:
            tokens = lex(src)
            self.assertEqual(
                tokens[1].type, expected_type,
                f"Failed for {src!r}: expected {expected_type}, got {tokens[1].type}"
            )
            # And the `=` part must not appear as a separate EQUAL token
            self.assertNotIn(TokenType.EQUAL, [t.type for t in tokens],
                             f"Stray EQUAL token in {src!r}")


if __name__ == "__main__":
    unittest.main()
