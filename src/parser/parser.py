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
            if self.current_token.value == 'def':
                return self.parse_function_definition()
            elif self.current_token.value == 'if':
                return self.parse_if_statement()
            elif self.current_token.value == 'for':
                return self.parse_for_statement()
            elif self.current_token.value == 'while':
                return self.parse_while_statement()
            elif self.current_token.value == 'return':
                return self.parse_return_statement()
            elif self.current_token.value == 'class':
                return self.parse_class_definition()
            elif self.current_token.value == 'import':
                return self.parse_import_statement()
            elif self.current_token.value == 'from':
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