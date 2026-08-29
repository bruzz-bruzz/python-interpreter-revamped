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
        statements = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
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
    
    def parse_expression(self, precedence: int = 0) -> Expression:
        """Parse an expression with given precedence"""
        left = self.parse_primary()
        
        while self.current_token.type != TokenType.EOF and self.get_precedence(self.current_token.type) > precedence:
            token = self.current_token
            self.advance()
            
            if token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE):
                right = self.parse_expression(self.get_precedence(token.type))
                left = BinaryExpression(left, token.type, right)
            elif token.type == TokenType.EQUAL:
                right = self.parse_expression()
                left = AssignmentExpression(left, right)
            elif token.type == TokenType.LPAREN:
                # Function call
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
        """Parse argument list for function calls"""
        args = []
        
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.parse_expression())
            
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                args.append(self.parse_expression())
        
        return args
    
    def get_precedence(self, token_type: TokenType) -> int:
        """Get precedence of an operator"""
        precedence = {
            TokenType.PLUS: 1,
            TokenType.MINUS: 1,
            TokenType.MULTIPLY: 2,
            TokenType.DIVIDE: 2,
            TokenType.EQUAL: 3,
        }
        return precedence.get(token_type, 0)

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
        """Parse an if statement: if condition: body [else: body]"""
        # 'if' keyword already consumed
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        else_body = None
        if (self.current_token.type == TokenType.KEYWORD
                and self.current_token.value in ('else', 'elif')):
            self.advance()  # consume 'else' or 'elif'
            self.expect(TokenType.COLON)
            else_body = self.parse_block()
        return IfStatement(condition, body, else_body)

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
        """Parse a block of statements terminated by NEWLINE/EOF."""
        statements: List[Statement] = []
        # Skip any leading newlines after the ':'
        while self.current_token.type == TokenType.NEWLINE:
            self.advance()
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            # Skip newlines between statements
            while self.current_token.type == TokenType.NEWLINE:
                self.advance()
            if self.current_token.type == TokenType.EOF:
                break
        return statements