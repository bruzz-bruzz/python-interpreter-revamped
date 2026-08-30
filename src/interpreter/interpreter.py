"""Tree-walking interpreter for our Python subset."""

from typing import Any, Dict, List, Optional

from src.ast import nodes as ast
from src.builtins.functions import BuiltInFunctions
from src.builtins.types import BuiltInTypes
from src.lexer.lexer import TokenType


class ReturnSignal(Exception):
    """Internal control-flow signal used to unwind the stack on `return`."""

    def __init__(self, value: Any):
        self.value = value


class Function:
    """A user-defined function object."""

    def __init__(self, name: str, parameters: List[str], body: List[ast.Statement],
                 closure: Dict[str, Any]):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure

    def __call__(self, interpreter: "Interpreter", arguments: List[Any]) -> Any:
        if len(arguments) != len(self.parameters):
            raise RuntimeError(
                f"Function {self.name!r} expected {len(self.parameters)} "
                f"argument(s) but got {len(arguments)}"
            )
        local_scope: Dict[str, Any] = dict(self.closure)
        for param, arg in zip(self.parameters, arguments):
            local_scope[param] = arg
        interpreter.push_scope(local_scope)
        try:
            for statement in self.body:
                interpreter.execute(statement)
            return None
        except ReturnSignal as ret:
            return ret.value
        finally:
            interpreter.pop_scope()

    def __repr__(self) -> str:
        return f"<function {self.name}>"


class Interpreter:
    """Executes an AST produced by the Parser."""

    def __init__(self) -> None:
        self.global_scope: Dict[str, Any] = {}
        self.scope_stack: List[Dict[str, Any]] = [self.global_scope]
        self._register_builtins()

    # Scope helpers
    def push_scope(self, scope: Dict[str, Any]) -> None:
        self.scope_stack.append(scope)

    def pop_scope(self) -> Dict[str, Any]:
        return self.scope_stack.pop()

    @property
    def current_scope(self) -> Dict[str, Any]:
        return self.scope_stack[-1]

    def _register_builtins(self) -> None:
        for name, func in BuiltInFunctions.all_functions().items():
            self.global_scope[name] = func
        for name, builtin_type in BuiltInTypes.all_types().items():
            self.global_scope[name] = builtin_type

    def interpret(self, program: ast.Program) -> None:
        for statement in program.statements:
            self.execute(statement)

    def execute(self, node: ast.ASTNode) -> Any:
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise RuntimeError(f"No visitor for AST node type: {type(node).__name__}")
        return visitor(node)

    # --- Variable / assignment ---
    def visit_Variable(self, node: ast.Variable) -> Any:
        name = node.name
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise NameError(f"Name {name!r} is not defined")

    def visit_AssignmentExpression(self, node: ast.AssignmentExpression) -> Any:
        if not isinstance(node.target, ast.Variable):
            raise RuntimeError("Assignment target must be a variable")
        value = self.execute(node.value)
        for scope in reversed(self.scope_stack):
            if node.target.name in scope:
                scope[node.target.name] = value
                return value
        self.current_scope[node.target.name] = value
        return value

    # --- Literals ---
    def visit_Integer(self, node: ast.Integer) -> int:
        return node.value

    def visit_Float(self, node: ast.Float) -> float:
        return node.value

    def visit_String(self, node: ast.String) -> str:
        return node.value

    def visit_Boolean(self, node: ast.Boolean) -> bool:
        return node.value

    def visit_NoneLiteral(self, node: ast.NoneLiteral) -> None:
        return None

    # --- Binary / Unary ---
    def visit_BinaryExpression(self, node: ast.BinaryExpression) -> Any:
        # Short-circuit logical operators: evaluate left first, only evaluate right
        # if the result depends on it.
        if node.operator == TokenType.KEYWORD and node.operator_value in ('and', 'or'):
            left = self.execute(node.left)
            if node.operator_value == 'and':
                if not self._is_truthy(left):
                    return left
                return self.execute(node.right)
            # 'or'
            if self._is_truthy(left):
                return left
            return self.execute(node.right)
        # Membership operator: `x in container`
        if node.operator == TokenType.KEYWORD and node.operator_value == 'in':
            left = self.execute(node.left)
            right = self.execute(node.right)
            if right is None:
                return False
            try:
                return left in right
            except TypeError:
                raise RuntimeError(
                    f"argument of type {type(right).__name__!r} is not iterable"
                )
        # Identity: `x is y` is equivalent to `id(x) == id(y)` here, but we
        # approximate it as `x is y` via `x == y` for built-in types.
        if node.operator == TokenType.KEYWORD and node.operator_value == 'is':
            left = self.execute(node.left)
            right = self.execute(node.right)
            return left is right
        left = self.execute(node.left)
        right = self.execute(node.right)
        op = node.operator
        try:
            if op == TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                return left + right
            if op == TokenType.MINUS:
                return left - right
            if op == TokenType.MULTIPLY:
                return left * right
            if op == TokenType.DIVIDE:
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
            if op == TokenType.INTEGER_DIVIDE:
                if right == 0:
                    raise RuntimeError("Division by zero")
                # Python's // already handles int/float properly
                return left // right
            if op == TokenType.MODULO:
                if right == 0:
                    raise RuntimeError("Modulo by zero")
                return left % right
            if op == TokenType.EQUAL_EQUAL:
                return left == right
            if op == TokenType.NOT_EQUAL:
                return left != right
            if op == TokenType.LESS:
                return left < right
            if op == TokenType.GREATER:
                return left > right
            if op == TokenType.LESS_EQUAL:
                return left <= right
            if op == TokenType.GREATER_EQUAL:
                return left >= right
        except TypeError as exc:
            raise RuntimeError(f"Type error in binary op {op.value}: {exc}")
        raise RuntimeError(f"Unsupported binary operator: {op.value}")

    def visit_ListLiteral(self, node: ast.ListLiteral) -> List[Any]:
        # Lists are just Python lists at runtime, which lets us reuse
        # iteration, len(), indexing, and slicing for free.
        return [self.execute(el) for el in node.elements]

    def visit_SubscriptExpression(self, node: ast.SubscriptExpression) -> Any:
        target = self.execute(node.target)
        index = self.execute(node.index)
        # Strings support indexing
        if isinstance(target, str):
            if not isinstance(index, int):
                raise TypeError(
                    f"String indices must be integers, not {type(index).__name__}"
                )
            # Support negative indices
            if index < 0:
                index += len(target)
            if index < 0 or index >= len(target):
                raise IndexError(f"string index out of range: {index}")
            return target[index]
        # Lists support indexing
        if isinstance(target, list):
            if not isinstance(index, int):
                raise TypeError(
                    f"List indices must be integers, not {type(index).__name__}"
                )
            if index < 0:
                index += len(target)
            if index < 0 or index >= len(target):
                raise IndexError(f"list index out of range: {index}")
            return target[index]
        raise TypeError(
            f"'{type(target).__name__}' object is not subscriptable"
        )

    def visit_UnaryExpression(self, node: ast.UnaryExpression) -> Any:
        operand = self.execute(node.operand)
        op = node.operator
        if op == TokenType.MINUS:
            return -operand
        if op == TokenType.PLUS:
            return +operand
        if op == TokenType.KEYWORD and node.operator_value == 'not':
            return not self._is_truthy(operand)
        raise RuntimeError(f"Unsupported unary operator: {op.value}")

    # --- Function call ---
    def visit_FunctionCall(self, node: ast.FunctionCall) -> Any:
        if not isinstance(node.function, ast.Variable):
            raise RuntimeError("Only simple name function calls are supported")
        name = node.function.name
        # Look up callable in any scope
        callee = None
        for scope in reversed(self.scope_stack):
            if name in scope:
                callee = scope[name]
                break
        if callee is None:
            raise NameError(f"Name {name!r} is not defined")
        args = [self.execute(arg) for arg in node.arguments]
        if isinstance(callee, Function):
            return callee(self, args)
        if callable(callee):
            return callee(*args)
        raise RuntimeError(f"Object {name!r} is not callable")

    # --- Statements ---
    def visit_ExpressionStatement(self, node: ast.ExpressionStatement) -> Any:
        return self.execute(node.expression)

    def visit_FunctionDefinition(self, node: ast.FunctionDefinition) -> None:
        func = Function(node.name, node.parameters, node.body,
                        closure=dict(self.current_scope))
        self.current_scope[node.name] = func
        return None

    def visit_IfStatement(self, node: ast.IfStatement) -> None:
        if self._is_truthy(self.execute(node.condition)):
            for stmt in node.body:
                self.execute(stmt)
        elif node.else_body is not None:
            for stmt in node.else_body:
                self.execute(stmt)

    def visit_WhileStatement(self, node: ast.WhileStatement) -> None:
        while self._is_truthy(self.execute(node.condition)):
            for stmt in node.body:
                self.execute(stmt)

    def visit_ForStatement(self, node: ast.ForStatement) -> None:
        iterable = self.execute(node.iterable)
        if not hasattr(iterable, "__iter__"):
            raise RuntimeError("For-loop target is not iterable")
        for value in iterable:
            self.current_scope[node.target] = value
            for stmt in node.body:
                self.execute(stmt)

    def visit_ReturnStatement(self, node: ast.ReturnStatement) -> None:
        value = None if node.value is None else self.execute(node.value)
        raise ReturnSignal(value)

    def visit_ClassDefinition(self, node: ast.ClassDefinition) -> None:
        # Minimal: just evaluate the body in a new scope to register any
        # methods/functions as attributes of the class dict.
        cls = {"__name__": node.name}
        self.current_scope[node.name] = cls
        for stmt in node.body:
            self.execute(stmt)

    def visit_ImportStatement(self, node: ast.ImportStatement) -> None:
        # Import is a no-op in this minimal interpreter. Bind the module name
        # to None so users can still write `import x` without erroring.
        self.current_scope[node.module] = None

    def visit_FromImportStatement(self, node: ast.FromImportStatement) -> None:
        self.current_scope[node.name] = None

    def visit_Block(self, node: ast.Block) -> None:
        for stmt in node.statements:
            self.execute(stmt)

    @staticmethod
    def _is_truthy(value: Any) -> bool:
        return bool(value)