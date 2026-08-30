"""Parser for Python interpreter - converts tokens into AST"""

from typing import List, Optional
from src.ast.nodes import *
from src.lexer.lexer import Token, TokenType


class Parser:
    """Python parser that builds AST from tokens"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def parse(self) -> Program:
        """Parse tokens into an AST Program"""
        statements: List[Statement] = []
        while self.current_token and self.current_token.type != TokenType.EOF:
            # Skip blank lines and stray DEDENTs at top level
            if self.current_token.type in (TokenType.NEWLINE, TokenType.DEDENT):
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[Statement]:
        """Parse a statement"""
        if self.current_token.type == TokenType.KEYWORD:
            keyword = self.current_token.value
            if keyword == 'def':
                self.advance()
                return self.parse_function_definition()
            elif keyword == 'if':
                self.advance()
                return self.parse_if_statement()
            elif keyword == 'for':
                self.advance()
                return self.parse_for_statement()
            elif keyword == 'while':
                self.advance()
                return self.parse_while_statement()
            elif keyword == 'return':
                self.advance()
                return self.parse_return_statement()
            elif keyword == 'class':
                self.advance()
                return self.parse_class_definition()
            elif keyword == 'import':
                self.advance()
                return self.parse_import_statement()
            elif keyword == 'from':
                self.advance()
                return self.parse_from_import_statement()

        # Default to expression statement
        return self.parse_expression_statement()
    
    def parse_expression_statement(self) -> ExpressionStatement:
        """Parse an expression statement"""
        node = self.parse_expression()
        return ExpressionStatement(node)

    def _current_precedence(self) -> int:
        """Get the precedence of the current token, taking into account
        keyword operators like 'and' and 'or' that share the KEYWORD type."""
        tok = self.current_token
        if tok.type == TokenType.KEYWORD and tok.value in ('and', 'or'):
            return self._keyword_precedence(tok.value)
        return self.get_precedence(tok.type)

    def parse_expression(self, precedence: int = 0) -> Expression:
        """Parse an expression using Pratt-style precedence climbing."""
        left = self.parse_primary()
        while (self.current_token.type != TokenType.EOF
               and self._current_precedence() > precedence):
            token = self.current_token
            token_prec = self._current_precedence()
            self.advance()
            if token.type in (TokenType.PLUS, TokenType.MINUS,
                              TokenType.MULTIPLY, TokenType.DIVIDE,
                              TokenType.INTEGER_DIVIDE, TokenType.MODULO,
                              TokenType.LESS, TokenType.GREATER,
                              TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL,
                              TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
                right = self.parse_expression(token_prec)
                left = BinaryExpression(left, token.type, right)
            elif (token.type == TokenType.KEYWORD
                  and token.value in ('and', 'or')):
                # Logical operator: store the keyword name on the AST node
                # so the interpreter can dispatch on it.
                right = self.parse_expression(token_prec)
                left = BinaryExpression(left, token.type, right,
                                        operator_value=token.value)
            elif token.type == TokenType.EQUAL:
                # Right-associative assignment
                right = self.parse_expression(token_prec - 1)
                left = AssignmentExpression(left, right)
            elif token.type == TokenType.LPAREN:
                # Function call (highest precedence, left-associative)
                args = self.parse_argument_list()
                left = FunctionCall(left, args)
        return left
    
    def parse_primary(self) -> Expression:
        """Parse a primary expression"""
        token = self.current_token
        
        if token.type == TokenType.INTEGER:
            self.advance()
            return Integer(token.value)
        elif token.type == TokenType.FLOAT:
            self.advance()
            return Float(token.value)
        elif token.type == TokenType.STRING:
            self.advance()
            return String(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(token.value)
        elif token.type == TokenType.KEYWORD:
            if token.value == 'True':
                self.advance()
                return Boolean(True)
            elif token.value == 'False':
                self.advance()
                return Boolean(False)
            elif token.value == 'None':
                self.advance()
                return NoneLiteral()
        
        raise SyntaxError(f"Unexpected token: {token.type} at line {token.line}")
    
    def parse_argument_list(self) -> List[Expression]:
        """Parse argument list for function calls. The opening '(' has
        already been consumed by parse_expression; we just parse the args
        and expect the closing ')'."""
        args: List[Expression] = []
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                args.append(self.parse_expression())
        self.expect(TokenType.RPAREN)
        return args
    
    def get_precedence(self, token_type: TokenType) -> int:
        """Get precedence of an operator. Higher number = tighter binding.

        For keyword operators like 'and' / 'or' the caller must look at the
        token's *value* since multiple keywords share the TokenType.KEYWORD
        type. We return a sentinel precedence (0) for KEYWORD here and let
        the caller inspect the value.
        """
        precedence = {
            TokenType.EQUAL: 1,           # lowest (assignment, right-assoc)
            TokenType.EQUAL_EQUAL: 3,     # comparisons
            TokenType.NOT_EQUAL: 3,
            TokenType.LESS: 3,
            TokenType.GREATER: 3,
            TokenType.LESS_EQUAL: 3,
            TokenType.GREATER_EQUAL: 3,
            TokenType.PLUS: 4,            # additive
            TokenType.MINUS: 4,
            TokenType.MULTIPLY: 5,        # multiplicative
            TokenType.DIVIDE: 5,
            TokenType.INTEGER_DIVIDE: 5,
            TokenType.MODULO: 5,
            TokenType.LPAREN: 10,         # function call (postfix)
        }
        return precedence.get(token_type, 0)

    def _keyword_precedence(self, value: str) -> int:
        """Precedence of keyword operators. 'or' binds looser than 'and',
        and both bind looser than any arithmetic / comparison operator."""
        if value == 'or':
            return 1   # lowest
        if value == 'and':
            return 2
        return 0

    def advance(self) -> None:
        """Advance to the next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Optional[Token]:
        """Peek at a token at a given offset without consuming it"""
        idx = self.pos + offset
        if 0 <= idx < len(self.tokens):
            return self.tokens[idx]
        return None

    def expect(self, token_type: TokenType) -> Token:
        """Consume the current token, asserting its type"""
        if self.current_token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.value} but got {self.current_token.type.value} "
                f"at line {self.current_token.line}, column {self.current_token.column}"
            )
        token = self.current_token
        self.advance()
        return token

    def match(self, token_type: TokenType) -> bool:
        """Check if current token matches the type, advance if so"""
        if self.current_token.type == token_type:
            self.advance()
            return True
        return False

    def parse_function_definition(self) -> FunctionDefinition:
        """Parse a function definition: def name(params): body"""
        # 'def' keyword has already been consumed by parse_statement
        if self.current_token.type != TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected function name but got {self.current_token.type.value} "
                f"at line {self.current_token.line}"
            )
        name = self.current_token.value
        self.advance()
        self.expect(TokenType.LPAREN)
        parameters = self.parse_parameter_list()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return FunctionDefinition(name, parameters, body)

    def parse_parameter_list(self) -> List[str]:
        """Parse comma-separated parameter names"""
        params = []
        if self.current_token.type != TokenType.RPAREN:
            if self.current_token.type != TokenType.IDENTIFIER:
                raise SyntaxError(
                    f"Expected parameter name but got {self.current_token.type.value} "
                    f"at line {self.current_token.line}"
                )
            params.append(self.current_token.value)
            self.advance()
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                if self.current_token.type != TokenType.IDENTIFIER:
                    raise SyntaxError(
                        f"Expected parameter name after comma at line {self.current_token.line}"
                    )
                params.append(self.current_token.value)
                self.advance()
        return params

    def parse_if_statement(self) -> IfStatement:
        """Parse an if statement with optional elif/else chain.

        Shape of the AST for `if c1: b1 elif c2: b2 elif c3: b3 else: b4`:
            IfStatement(c1, b1, else_body=[
                IfStatement(c2, b2, else_body=[
                    IfStatement(c3, b3, else_body=b4)
                ])
            ])
        """
        # 'if' keyword already consumed
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()

        # Build the elif chain. We start with the outer IfStatement and
        # link each new 'elif' as a nested IfStatement inside the previous
        # one's else_body. A final 'else' attaches as the else_body of the
        # last IfStatement in the chain.
        outer = IfStatement(condition, body, None)
        current = outer
        while (self.current_token.type == TokenType.KEYWORD
                and self.current_token.value in ('elif', 'else')):
            if self.current_token.value == 'elif':
                self.advance()  # consume 'elif'
                elif_condition = self.parse_expression()
                self.expect(TokenType.COLON)
                elif_body = self.parse_block()
                new_if = IfStatement(elif_condition, elif_body, None)
                current.else_body = [new_if]
                current = new_if
            else:
                # 'else' clause - no condition
                self.advance()  # consume 'else'
                self.expect(TokenType.COLON)
                current.else_body = self.parse_block()
                # Chain ends here
                break
        return outer

    def parse_for_statement(self) -> ForStatement:
        """Parse a for loop: for target in iterable: body"""
        # 'for' keyword already consumed
        if self.current_token.type != TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected variable name after 'for' but got "
                f"{self.current_token.type.value} at line {self.current_token.line}"
            )
        target = self.current_token.value
        self.advance()
        if not (self.current_token.type == TokenType.KEYWORD
                and self.current_token.value == 'in'):
            raise SyntaxError(
                f"Expected 'in' after for-loop variable at line {self.current_token.line}"
            )
        self.advance()
        iterable = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return ForStatement(target, iterable, body)

    def parse_while_statement(self) -> WhileStatement:
        """Parse a while loop: while condition: body"""
        # 'while' keyword already consumed
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_return_statement(self) -> ReturnStatement:
        """Parse a return statement: return [value]"""
        # 'return' keyword already consumed
        value = None
        if self.current_token.type not in (TokenType.NEWLINE, TokenType.EOF,
                                            TokenType.COLON, TokenType.SEMICOLON):
            value = self.parse_expression()
        return ReturnStatement(value)

    def parse_class_definition(self) -> ClassDefinition:
        """Parse a class definition: class Name: body"""
        # 'class' keyword already consumed
        if self.current_token.type != TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected class name but got {self.current_token.type.value} "
                f"at line {self.current_token.line}"
            )
        name = self.current_token.value
        self.advance()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return ClassDefinition(name, body)

    def parse_import_statement(self) -> ImportStatement:
        """Parse an import statement: import module"""
        # 'import' keyword already consumed
        if self.current_token.type != TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected module name after 'import' at line {self.current_token.line}"
            )
        module = self.current_token.value
        self.advance()
        return ImportStatement(module)

    def parse_from_import_statement(self) -> FromImportStatement:
        """Parse a from-import statement: from module import name"""
        # 'from' keyword already consumed
        if self.current_token.type != TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected module name after 'from' at line {self.current_token.line}"
            )
        module = self.current_token.value
        self.advance()
        if not (self.current_token.type == TokenType.KEYWORD
                and self.current_token.value == 'import'):
            raise SyntaxError(
                f"Expected 'import' after module name at line {self.current_token.line}"
            )
        self.advance()
        if self.current_token.type != TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected name to import at line {self.current_token.line}"
            )
        name = self.current_token.value
        self.advance()
        return FromImportStatement(module, name)

    def parse_block(self) -> List[Statement]:
        """Parse an indented block. Expects the current token to be NEWLINE,
        then INDENT, then a sequence of statements, then a matching DEDENT."""
        statements: List[Statement] = []
        # Skip optional blank lines after the ':'
        while self.current_token.type == TokenType.NEWLINE:
            self.advance()
        if self.current_token.type != TokenType.INDENT:
            # Single-line block (e.g. on the same line as ':')
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            return statements
        self.advance()  # consume INDENT
        while self.current_token.type not in (TokenType.DEDENT, TokenType.EOF):
            # Skip stray newlines between statements
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            # Skip newlines after each statement
            while self.current_token.type == TokenType.NEWLINE:
                self.advance()
        if self.current_token.type == TokenType.DEDENT:
            self.advance()
        return statements