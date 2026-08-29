"""Lexer for Python interpreter - converts source code into tokens"""

import re
from enum import Enum
from typing import List, Optional, Tuple


class TokenType(Enum):
    """Token types for Python language"""
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Punctuation
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    DOT = "DOT"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"


class Token:
    """Token class representing a token in the source code"""
    
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self) -> str:
        return f"Token({self.type.value}, {repr(self.value)}, line {self.line}, col {self.column})"
    
    def __repr__(self) -> str:
        return self.__str__()


class Lexer:
    """Python lexer that tokenizes source code"""
    
    # Python keywords
    KEYWORDS = {
        'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return',
        'import', 'from', 'as', 'pass', 'break', 'continue', 'in', 'is',
        'and', 'or', 'not', 'True', 'False', 'None', 'try', 'except',
        'finally', 'raise', 'with', 'global', 'nonlocal', 'lambda'
    }
    
    # Regular expressions for token matching
    token_specification = [
        ('INTEGER', r'\d+'),
        ('FLOAT', r'\d+\.\d*'),
        ('STRING', r'"[^"]*"|\'[^\']*\''),  # Handle both " and ' strings
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('EQUAL_EQUAL', r'=='),
        ('NOT_EQUAL', r'!='),
        ('LESS_EQUAL', r'<='),
        ('GREATER_EQUAL', r'>='),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULTIPLY', r'\*'),
        ('DIVIDE', r'/'),
        ('EQUAL', r'='),
        ('LESS', r'<'),
        ('GREATER', r'>'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('COMMA', r','),
        ('COLON', r':'),
        ('SEMICOLON', r';'),
        ('DOT', r'\.'),
        ('NEWLINE', r'\n'),
        ('COMMENT', r'#.*'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.line = 1
        self.column = 1
        self.pos = 0
        self.build_token_specification()
    
    def build_token_specification(self):
        """Build regex patterns for tokens"""
        self.token_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification))
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code"""
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        
        while self.pos < len(self.source):
            match = self.token_regex.match(self.source, self.pos)
            if not match:
                raise SyntaxError(f"Illegal character at line {self.line}, column {self.column}: {self.source[self.pos]}")
            
            token_type = match.lastgroup
            value = match.group()
            
            if token_type == 'INTEGER':
                token = Token(TokenType.INTEGER, int(value), self.line, self.column)
            elif token_type == 'FLOAT':
                token = Token(TokenType.FLOAT, float(value), self.line, self.column)
            elif token_type == 'STRING':
                # Remove quotes
                token = Token(TokenType.STRING, value.strip('\"\''), self.line, self.column)
            elif token_type == 'IDENTIFIER':
                if value in self.KEYWORDS:
                    token = Token(TokenType.KEYWORD, value, self.line, self.column)
                else:
                    token = Token(TokenType.IDENTIFIER, value, self.line, self.column)
            elif token_type == 'NEWLINE':
                token = Token(TokenType.NEWLINE, value, self.line, self.column)
                self.line += 1
                self.column = 1
            elif token_type == 'SKIP':
                # Skip whitespace
                pass
            elif token_type == 'COMMENT':
                token = Token(TokenType.COMMENT, value, self.line, self.column)
            elif token_type == 'MISMATCH':
                raise SyntaxError(f"Illegal character at line {self.line}, column {self.column}: {value}")
            else:
                # Handle punctuation and operators
                token_type_enum = self._get_token_type_from_string(token_type)
                token = Token(token_type_enum, value, self.line, self.column)
            
            if token_type != 'SKIP':
                self.tokens.append(token)
            
            self.pos = match.end()
            self.column += len(value)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _get_token_type_from_string(self, type_str: str) -> TokenType:
        """Convert string token type to TokenType enum"""
        try:
            return TokenType(type_str)
        except ValueError:
            # Handle special cases
            if type_str == 'LBRACKET':
                return TokenType.LBRACKET
            elif type_str == 'RBRACKET':
                return TokenType.RBRACKET
            raise