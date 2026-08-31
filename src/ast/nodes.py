"""AST node definitions for Python interpreter"""

from typing import Any, List, Optional, Tuple as TupleType
from src.lexer.lexer import TokenType


class ASTNode:
    """Base class for all AST nodes"""

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return self.__str__()


class Expression(ASTNode):
    """Base class for all expressions"""
    pass


class Statement(ASTNode):
    """Base class for all statements"""
    pass


class Program(ASTNode):
    """Root node representing the entire program"""

    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def __str__(self) -> str:
        return f"Program({len(self.statements)} statements)"


# === Literal Expressions ===

class Integer(Expression):
    """Integer literal"""

    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return f"Integer({self.value})"


class Float(Expression):
    """Float literal"""

    def __init__(self, value: float):
        self.value = value

    def __str__(self) -> str:
        return f"Float({self.value})"


class String(Expression):
    """String literal"""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return f"String({repr(self.value)})"


class Boolean(Expression):
    """Boolean literal"""

    def __init__(self, value: bool):
        self.value = value

    def __str__(self) -> str:
        return f"Boolean({self.value})"


class NoneLiteral(Expression):
    """None literal"""

    def __str__(self) -> str:
        return "None"


# === Variable and Identifier Expressions ===

class Variable(Expression):
    """Variable reference"""

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"Variable({self.name})"


# === Binary and Unary Expressions ===

class BinaryExpression(Expression):
    """Binary operation (e.g., a + b)

    `operator` is a TokenType for normal operators. For the logical
    keyword operators 'and' / 'or', `operator` is set to TokenType.KEYWORD
    and `operator_value` holds the actual keyword string ('and' or 'or').
    """

    def __init__(self, left: Expression, operator: TokenType, right: Expression,
                 operator_value: Optional[str] = None):
        self.left = left
        self.operator = operator
        self.right = right
        self.operator_value = operator_value

    def __str__(self) -> str:
        op_name = self.operator_value or self.operator.value
        return f"BinaryOp({self.left} {op_name} {self.right})"


class UnaryExpression(Expression):
    """Unary operation (e.g., -x, not x)

    `operator` is a TokenType for normal operators. For the keyword
    operator 'not', `operator` is set to TokenType.KEYWORD and
    `operator_value` holds the string 'not'.
    """

    def __init__(self, operator: TokenType, operand: Expression,
                 operator_value: Optional[str] = None):
        self.operator = operator
        self.operand = operand
        self.operator_value = operator_value

    def __str__(self) -> str:
        op_name = self.operator_value or self.operator.value
        return f"UnaryOp({op_name} {self.operand})"


class AssignmentExpression(Expression):
    """Assignment expression (e.g., x = 5)"""

    def __init__(self, target: Expression, value: Expression):
        self.target = target
        self.value = value

    def __str__(self) -> str:
        return f"Assign({self.target} = {self.value})"


class AugmentedAssignmentExpression(Expression):
    """Augmented assignment expression (e.g., x += 1, x *= 2)"""

    def __init__(self, target: Expression, operator: TokenType, value: Expression):
        self.target = target
        self.operator = operator
        self.value = value

    def __str__(self) -> str:
        return f"AugAssign({self.target} {self.operator.value} {self.value})"


# === Function Call ===

class FunctionCall(Expression):
    """Function call expression (e.g., foo(1, 2))"""

    def __init__(self, function: Expression, arguments: List[Expression]):
        self.function = function
        self.arguments = arguments

    def __str__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"Call({self.function}({args_str}))"


class SubscriptExpression(Expression):
    """Subscript / indexing expression (e.g., arr[0], s[1])"""

    def __init__(self, target: Expression, index: Expression):
        self.target = target
        self.index = index

    def __str__(self) -> str:
        return f"Subscript({self.target}[{self.index}])"


class AttributeAccess(Expression):
    """Attribute access expression (e.g., obj.attr, s.upper).

    This represents a method/property reference on an object. When followed
    by `(...)` it is invoked as a method call (see MethodCall).
    """

    def __init__(self, target: Expression, attribute: str):
        self.target = target
        self.attribute = attribute

    def __str__(self) -> str:
        return f"Attr({self.target}.{self.attribute})"


class MethodCall(Expression):
    """Method call expression (e.g., s.upper(), "a,b".split(","))"""

    def __init__(self, target: Expression, method: str,
                 arguments: List[Expression]):
        self.target = target
        self.method = method
        self.arguments = arguments

    def __str__(self) -> str:
        args_str = ", ".join(str(a) for a in self.arguments)
        return f"MethodCall({self.target}.{self.method}({args_str}))"


class ListLiteral(Expression):
    """List literal expression (e.g., [1, 2, 3])"""

    def __init__(self, elements: List[Expression]):
        self.elements = elements

    def __str__(self) -> str:
        return f"List([{', '.join(str(e) for e in self.elements)}])"


class TupleLiteral(Expression):
    """Tuple literal expression (e.g., (1, 2), (), (42,))

    Tuples are immutable, ordered collections.
    """

    def __init__(self, elements: List[Expression]):
        self.elements = elements

    def __str__(self) -> str:
        return f"Tuple(({', '.join(str(e) for e in self.elements)}))"


class DictLiteral(Expression):
    """Dictionary literal expression (e.g., {"a": 1, "b": 2}).

    Dictionaries are mutable, unordered key-value maps.
    """

    def __init__(self, entries: List[TupleType[Expression, Expression]]):
        self.entries = entries  # list of (key, value) pairs

    def __str__(self) -> str:
        pairs = ", ".join(f"{k}: {v}" for k, v in self.entries)
        return f"Dict({{{pairs}}})"


class SetLiteral(Expression):
    """Set literal expression (e.g., {1, 2, 3}).

    Sets are mutable, unordered collections of unique, hashable elements.
    """

    def __init__(self, elements: List[Expression]):
        self.elements = elements

    def __str__(self) -> str:
        return f"Set({{{', '.join(str(e) for e in self.elements)}}})"


# === Statements ===

class ExpressionStatement(Statement):
    """Statement that is just an expression"""

    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self) -> str:
        return f"ExprStmt({self.expression})"


class FunctionDefinition(Statement):
    """Function definition (e.g., def foo(x): ...)"""

    def __init__(self, name: str, parameters: List[str], body: List[Statement]):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __str__(self) -> str:
        params_str = ", ".join(self.parameters)
        return f"FunctionDef({self.name}({params_str}))"


class IfStatement(Statement):
    """If statement"""

    def __init__(self, condition: Expression, body: List[Statement],
                 else_body: Optional[List[Statement]] = None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __str__(self) -> str:
        return f"If({self.condition})"


class ForStatement(Statement):
    """For loop statement (e.g., for x in iterable: ...)"""

    def __init__(self, target: str, iterable: Expression, body: List[Statement]):
        self.target = target
        self.iterable = iterable
        self.body = body

    def __str__(self) -> str:
        return f"For({self.target} in {self.iterable})"


class WhileStatement(Statement):
    """While loop statement"""

    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return f"While({self.condition})"


class ReturnStatement(Statement):
    """Return statement"""

    def __init__(self, value: Optional[Expression]):
        self.value = value

    def __str__(self) -> str:
        return f"Return({self.value})"


class BreakStatement(Statement):
    """`break` statement: exit the innermost loop."""

    def __str__(self) -> str:
        return "Break()"


class ContinueStatement(Statement):
    """`continue` statement: skip to the next iteration of the innermost loop."""

    def __str__(self) -> str:
        return "Continue()"


class ClassDefinition(Statement):
    """Class definition (e.g., class Foo: ...)"""

    def __init__(self, name: str, body: List[Statement]):
        self.name = name
        self.body = body

    def __str__(self) -> str:
        return f"ClassDef({self.name})"


class ImportStatement(Statement):
    """Import statement (e.g., import foo)"""

    def __init__(self, module: str):
        self.module = module

    def __str__(self) -> str:
        return f"Import({self.module})"


class FromImportStatement(Statement):
    """From import statement (e.g., from foo import bar)"""

    def __init__(self, module: str, name: str):
        self.module = module
        self.name = name

    def __str__(self) -> str:
        return f"FromImport({self.module} import {self.name})"


class Block(Statement):
    """Block of statements"""

    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def __str__(self) -> str:
        return f"Block({len(self.statements)} statements)"
