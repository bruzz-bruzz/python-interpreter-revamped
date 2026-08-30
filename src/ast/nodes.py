"""AST node definitions for Python interpreter"""

from typing import Any, List, Optional
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
    """Unary operation (e.g., -x, not x)"""

    def __init__(self, operator: TokenType, operand: Expression):
        self.operator = operator
        self.operand = operand

    def __str__(self) -> str:
        return f"UnaryOp({self.operator.value} {self.operand})"


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
