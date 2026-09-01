/**
 * TypeScript port of `src/parser/parser.py`.
 *
 * Recursive-descent / Pratt-style precedence-climbing parser that builds
 * an AST from a token stream.
 */

import { Token, TokenType } from './lexer';
import {
  ASTNode, Expression, Statement,
  Program, ProgramNode, ExpressionStatement, FunctionDefinition, IfStatement,
  ForStatement, WhileStatement, ReturnStatement, BreakStatement,
  ContinueStatement, ClassDefinition, ImportStatement, FromImportStatement,
  Block, Integer, Float, Str, Bool, NoneLit, Variable,
  BinaryExpression, UnaryExpression, AssignmentExpression,
  FunctionCall, SubscriptExpression, AttributeAccess, MethodCall,
  ListLiteral, TupleLiteral, DictLiteral, SetLiteral,
  AnyExpression, AnyStatement,
} from './ast';

export class Parser {
  private tokens: Token[];
  private pos = 0;
  private current_token: Token | null;

  constructor(tokens: Token[]) {
    this.tokens = tokens;
    this.current_token = tokens.length > 0 ? tokens[0] : null;
  }

  private advance(): void {
    if (this.pos < this.tokens.length - 1) {
      this.pos += 1;
      this.current_token = this.tokens[this.pos];
    }
  }

  private peek(offset = 1): Token | null {
    const idx = this.pos + offset;
    if (idx >= 0 && idx < this.tokens.length) return this.tokens[idx];
    return null;
  }

  private expect(token_type: TokenType): Token {
    if (!this.current_token || this.current_token.type !== token_type) {
      const got = this.current_token ? this.current_token.type : 'EOF';
      const line = this.current_token?.line ?? 0;
      const column = this.current_token?.column ?? 0;
      throw new SyntaxError(
        `Expected ${token_type} but got ${got} at line ${line}, column ${column}`
      );
    }
    const token = this.current_token;
    this.advance();
    return token;
  }

  private match(token_type: TokenType): boolean {
    if (this.current_token && this.current_token.type === token_type) {
      this.advance();
      return true;
    }
    return false;
  }

  private getPrecedence(token_type: TokenType): number {
    const precedence: Partial<Record<TokenType, number>> = {
      [TokenType.EQUAL]: 1,
      [TokenType.PLUSEQUAL]: 1,
      [TokenType.MINUSEQUAL]: 1,
      [TokenType.MULTIPLYEQUAL]: 1,
      [TokenType.DIVIDEEQUAL]: 1,
      [TokenType.INTEGERDIVIDEEQUAL]: 1,
      [TokenType.MODULOEQUAL]: 1,
      [TokenType.EQUAL_EQUAL]: 3,
      [TokenType.NOT_EQUAL]: 3,
      [TokenType.LESS]: 3,
      [TokenType.GREATER]: 3,
      [TokenType.LESS_EQUAL]: 3,
      [TokenType.GREATER_EQUAL]: 3,
      [TokenType.PLUS]: 4,
      [TokenType.MINUS]: 4,
      [TokenType.MULTIPLY]: 5,
      [TokenType.DIVIDE]: 5,
      [TokenType.INTEGER_DIVIDE]: 5,
      [TokenType.MODULO]: 5,
      [TokenType.LPAREN]: 10,
      [TokenType.LBRACKET]: 10,
      [TokenType.DOT]: 10,
    };
    return precedence[token_type] ?? 0;
  }

  private keywordPrecedence(value: string): number {
    if (value === 'or') return 1;
    if (value === 'and') return 2;
    if (value === 'in' || value === 'not' || value === 'is') return 3;
    return 0;
  }

  private currentPrecedence(): number {
    const tok = this.current_token;
    if (!tok) return 0;
    if (tok.type === TokenType.KEYWORD) {
      const value = tok.value as string;
      if (value === 'and' || value === 'or' || value === 'in' || value === 'is') {
        return this.keywordPrecedence(value);
      }
      if (value === 'not') {
        const next = this.peek(1);
        if (
          next && next.type === TokenType.KEYWORD &&
          (next.value as string) === 'in'
        ) {
          return 3;
        }
      }
    }
    return this.getPrecedence(tok.type);
  }

  parse(): ProgramNode {
    const statements: Statement[] = [];
    while (this.current_token && (this.current_token?.type as TokenType) !== TokenType.EOF) {
      if (
        (this.current_token?.type as TokenType) === TokenType.NEWLINE ||
        (this.current_token?.type as TokenType) === TokenType.DEDENT
      ) {
        this.advance();
        continue;
      }
      const stmt = this.parseStatement();
      if (stmt) statements.push(stmt);
    }
    return Program(statements);
  }

  private parseStatement(): Statement | null {
    if (this.current_token && (this.current_token?.type as TokenType) === TokenType.KEYWORD) {
      const keyword = this.current_token.value as string;
      if (keyword === 'def') { this.advance(); return this.parseFunctionDefinition(); }
      if (keyword === 'if')  { this.advance(); return this.parseIfStatement(); }
      if (keyword === 'for') { this.advance(); return this.parseForStatement(); }
      if (keyword === 'while') { this.advance(); return this.parseWhileStatement(); }
      if (keyword === 'return') { this.advance(); return this.parseReturnStatement(); }
      if (keyword === 'break') { this.advance(); return BreakStatement(); }
      if (keyword === 'continue') { this.advance(); return ContinueStatement(); }
      if (keyword === 'class') { this.advance(); return this.parseClassDefinition(); }
      if (keyword === 'import') { this.advance(); return this.parseImportStatement(); }
      if (keyword === 'from') { this.advance(); return this.parseFromImportStatement(); }
    }
    return this.parseExpressionStatement();
  }

  private parseExpressionStatement(): Statement {
    const node = this.parseExpression();
    return ExpressionStatement(node);
  }

  private parseExpression(precedence = 0): Expression {
    let left = this.parsePrimary();
    while (
      this.current_token &&
      (this.current_token?.type as TokenType) !== TokenType.EOF &&
      this.currentPrecedence() > precedence
    ) {
      const token = this.current_token;
      const tokenPrec = this.currentPrecedence();
      const isPostfix =
        token.type === TokenType.LPAREN ||
        token.type === TokenType.LBRACKET ||
        token.type === TokenType.DOT;
      if (!isPostfix) this.advance();

      const tokenValue = token.value as string;
      const isArithOrCmp =
        token.type === TokenType.PLUS || token.type === TokenType.MINUS ||
        token.type === TokenType.MULTIPLY || token.type === TokenType.DIVIDE ||
        token.type === TokenType.INTEGER_DIVIDE || token.type === TokenType.MODULO ||
        token.type === TokenType.LESS || token.type === TokenType.GREATER ||
        token.type === TokenType.LESS_EQUAL || token.type === TokenType.GREATER_EQUAL ||
        token.type === TokenType.EQUAL_EQUAL || token.type === TokenType.NOT_EQUAL;
      if (isArithOrCmp) {
        const right = this.parseExpression(tokenPrec);
        left = BinaryExpression(left, token.type, right);
      } else if (
        token.type === TokenType.KEYWORD &&
        (tokenValue === 'and' || tokenValue === 'or' ||
         tokenValue === 'in'  || tokenValue === 'is')
      ) {
        const right = this.parseExpression(tokenPrec);
        left = BinaryExpression(left, token.type, right, tokenValue);
      } else if (
        token.type === TokenType.KEYWORD && tokenValue === 'not' &&
        this.current_token && (this.current_token?.type as TokenType) === TokenType.KEYWORD &&
        (this.current_token.value as string) === 'in'
      ) {
        this.advance(); // consume 'in'
        const right = this.parseExpression(tokenPrec);
        left = BinaryExpression(left, TokenType.KEYWORD, right, 'not in');
      } else if (token.type === TokenType.EQUAL) {
        const right = this.parseExpression(tokenPrec - 1);
        left = AssignmentExpression(left, right);
      } else if (
        token.type === TokenType.PLUSEQUAL || token.type === TokenType.MINUSEQUAL ||
        token.type === TokenType.MULTIPLYEQUAL || token.type === TokenType.DIVIDEEQUAL ||
        token.type === TokenType.INTEGERDIVIDEEQUAL || token.type === TokenType.MODULOEQUAL
      ) {
        if (left.kind !== 'Variable') {
          throw new SyntaxError(
            `Augmented assignment target must be a variable at line ${token.line}`
          );
        }
        const underlying: Record<string, TokenType> = {
          [TokenType.PLUSEQUAL]: TokenType.PLUS,
          [TokenType.MINUSEQUAL]: TokenType.MINUS,
          [TokenType.MULTIPLYEQUAL]: TokenType.MULTIPLY,
          [TokenType.DIVIDEEQUAL]: TokenType.DIVIDE,
          [TokenType.INTEGERDIVIDEEQUAL]: TokenType.INTEGER_DIVIDE,
          [TokenType.MODULOEQUAL]: TokenType.MODULO,
        };
        const op = underlying[token.type];
        const right = this.parseExpression(tokenPrec - 1);
        const newValue = BinaryExpression(left, op, right);
        left = AssignmentExpression(left, newValue);
      } else if (token.type === TokenType.LPAREN) {
        this.advance();
        const args = this.parseArgumentList();
        left = FunctionCall(left, args);
      } else if (token.type === TokenType.LBRACKET) {
        this.advance();
        const index_expr = this.parseExpression();
        this.expect(TokenType.RBRACKET);
        left = SubscriptExpression(left, index_expr);
      } else if (token.type === TokenType.DOT) {
        this.advance();
        if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
          throw new SyntaxError(
            `Expected attribute name after '.' at line ${this.current_token?.line ?? 0}`
          );
        }
        const attr = this.current_token.value as string;
        this.advance();
        if (this.current_token && (this.current_token?.type as TokenType) === TokenType.LPAREN) {
          this.advance();
          const args = this.parseArgumentList();
          left = MethodCall(left, attr, args);
        } else {
          left = AttributeAccess(left, attr);
        }
      } else {
        break;
      }
    }
    return left;
  }

  private parsePrimary(): Expression {
    const token = this.current_token;
    if (!token) throw new SyntaxError('Unexpected end of input');

    // Unary prefix operators
    if (token.type === TokenType.MINUS) {
      this.advance();
      const operand = this.parsePrimary();
      return UnaryExpression(TokenType.MINUS, operand);
    }
    if (token.type === TokenType.PLUS) {
      this.advance();
      const operand = this.parsePrimary();
      return UnaryExpression(TokenType.PLUS, operand);
    }
    if (token.type === TokenType.KEYWORD && (token.value as string) === 'not') {
      this.advance();
      const operand = this.parsePrimary();
      return UnaryExpression(TokenType.KEYWORD, operand, 'not');
    }

    if (token.type === TokenType.LPAREN) {
      this.advance();
      if (this.current_token && (this.current_token?.type as TokenType) === TokenType.RPAREN) {
        this.advance();
        return TupleLiteral([]);
      }
      const first: Expression = this.parseExpression();
      if (this.current_token && (this.current_token?.type as TokenType) === TokenType.COMMA) {
        this.advance();
        const elements: Expression[] = [first];
        while (this.current_token && (this.current_token?.type as TokenType) !== TokenType.RPAREN) {
          elements.push(this.parseExpression());
          if (this.current_token && (this.current_token?.type as TokenType) === TokenType.COMMA) {
            this.advance();
          } else {
            break;
          }
        }
        this.expect(TokenType.RPAREN);
        return TupleLiteral(elements);
      }
      this.expect(TokenType.RPAREN);
      return first;
    }

    if (token.type === TokenType.LBRACKET) {
      this.advance();
      const elements: Expression[] = [];
      if (this.current_token && (this.current_token?.type as TokenType) !== TokenType.RBRACKET) {
        elements.push(this.parseExpression());
        while (this.current_token && (this.current_token?.type as TokenType) === TokenType.COMMA) {
          this.advance();
          if (this.current_token && (this.current_token?.type as TokenType) === TokenType.RBRACKET) break;
          elements.push(this.parseExpression());
        }
      }
      this.expect(TokenType.RBRACKET);
      return ListLiteral(elements);
    }

    if (token.type === TokenType.LBRACE) {
      this.advance();
      if (this.current_token && (this.current_token?.type as TokenType) === TokenType.RBRACE) {
        this.advance();
        return DictLiteral([]);
      }
      const first = this.parseExpression();
      if (this.current_token && (this.current_token?.type as TokenType) === TokenType.COLON) {
        this.advance();
        const entries: Array<[Expression, Expression]> = [];
        const value = this.parseExpression();
        entries.push([first, value]);
        while (this.current_token && (this.current_token?.type as TokenType) === TokenType.COMMA) {
          this.advance();
          if (this.current_token && (this.current_token?.type as TokenType) === TokenType.RBRACE) break;
          const k = this.parseExpression();
          this.expect(TokenType.COLON);
          const v = this.parseExpression();
          entries.push([k, v]);
        }
        this.expect(TokenType.RBRACE);
        return DictLiteral(entries);
      }
      const elements: Expression[] = [first];
      while (this.current_token && (this.current_token?.type as TokenType) === TokenType.COMMA) {
        this.advance();
        if (this.current_token && (this.current_token?.type as TokenType) === TokenType.RBRACE) break;
        elements.push(this.parseExpression());
      }
      this.expect(TokenType.RBRACE);
      return SetLiteral(elements);
    }

    if (token.type === TokenType.INTEGER) {
      this.advance();
      return Integer(token.value as number);
    }
    if (token.type === TokenType.FLOAT) {
      this.advance();
      return Float(token.value as number);
    }
    if (token.type === TokenType.STRING) {
      this.advance();
      return Str(token.value as string);
    }
    if (token.type === TokenType.IDENTIFIER) {
      const name = token.value as string;
      this.advance();
      return Variable(name);
    }
    if (token.type === TokenType.KEYWORD) {
      const value = token.value as string;
      if (value === 'True') { this.advance(); return Bool(true); }
      if (value === 'False') { this.advance(); return Bool(false); }
      if (value === 'None') { this.advance(); return NoneLit(); }
    }

    throw new SyntaxError(
      `Unexpected token: ${token.type} at line ${token.line}`
    );
  }

  private parseArgumentList(): Expression[] {
    const args: Expression[] = [];
    if (this.current_token && (this.current_token?.type as TokenType) !== TokenType.RPAREN) {
      args.push(this.parseExpression());
      while (this.current_token && (this.current_token?.type as TokenType) === TokenType.COMMA) {
        this.advance();
        args.push(this.parseExpression());
      }
    }
    this.expect(TokenType.RPAREN);
    return args;
  }

  private parseFunctionDefinition(): Statement {
    if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
      throw new SyntaxError(
        `Expected function name but got ${this.current_token?.type} at line ${this.current_token?.line}`
      );
    }
    const name = this.current_token.value as string;
    this.advance();
    this.expect(TokenType.LPAREN);
    const parameters = this.parseParameterList();
    this.expect(TokenType.RPAREN);
    this.expect(TokenType.COLON);
    const body = this.parseBlock();
    return FunctionDefinition(name, parameters, body);
  }

  private parseParameterList(): string[] {
    const params: string[] = [];
    if (this.current_token && (this.current_token?.type as TokenType) !== TokenType.RPAREN) {
      if ((this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
        throw new SyntaxError(
          `Expected parameter name but got ${this.current_token.type} at line ${this.current_token.line}`
        );
      }
      params.push(this.current_token.value as string);
      this.advance();
      while (this.current_token && (this.current_token?.type as TokenType) === TokenType.COMMA) {
        this.advance();
        if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
          throw new SyntaxError(
            `Expected parameter name after comma at line ${this.current_token?.line}`
          );
        }
        params.push(this.current_token.value as string);
        this.advance();
      }
    }
    return params;
  }

  private parseIfStatement(): Statement {
    const condition = this.parseExpression();
    this.expect(TokenType.COLON);
    const body = this.parseBlock();

    const outer = IfStatement(condition, body, undefined);
    let current = outer;
    while (
      this.current_token &&
      (this.current_token?.type as TokenType) === TokenType.KEYWORD &&
      ((this.current_token.value as string) === 'elif' ||
       (this.current_token.value as string) === 'else')
    ) {
      const kw = this.current_token.value as string;
      if (kw === 'elif') {
        this.advance();
        const elifCondition = this.parseExpression();
        this.expect(TokenType.COLON);
        const elifBody = this.parseBlock();
        const newIf = IfStatement(elifCondition, elifBody, undefined);
        current.elseBody = [newIf];
        current = newIf;
      } else {
        this.advance();
        this.expect(TokenType.COLON);
        current.elseBody = this.parseBlock();
        break;
      }
    }
    return outer;
  }

  private parseForStatement(): Statement {
    if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
      throw new SyntaxError(
        `Expected variable name after 'for' but got ${this.current_token?.type} at line ${this.current_token?.line}`
      );
    }
    const target = this.current_token.value as string;
    this.advance();
    if (!(
      this.current_token &&
      (this.current_token?.type as TokenType) === TokenType.KEYWORD &&
      (this.current_token.value as string) === 'in'
    )) {
      throw new SyntaxError(
        `Expected 'in' after for-loop variable at line ${this.current_token?.line}`
      );
    }
    this.advance();
    const iterable = this.parseExpression();
    this.expect(TokenType.COLON);
    const body = this.parseBlock();
    return ForStatement(target, iterable, body);
  }

  private parseWhileStatement(): Statement {
    const condition = this.parseExpression();
    this.expect(TokenType.COLON);
    const body = this.parseBlock();
    return WhileStatement(condition, body);
  }

  private parseReturnStatement(): Statement {
    let value: Expression | null = null;
    if (
      this.current_token &&
      (this.current_token?.type as TokenType) !== TokenType.NEWLINE &&
      (this.current_token?.type as TokenType) !== TokenType.EOF &&
      (this.current_token?.type as TokenType) !== TokenType.COLON &&
      (this.current_token?.type as TokenType) !== TokenType.SEMICOLON
    ) {
      value = this.parseExpression();
    }
    return ReturnStatement(value);
  }

  private parseClassDefinition(): Statement {
    if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
      throw new SyntaxError(
        `Expected class name but got ${this.current_token?.type} at line ${this.current_token?.line}`
      );
    }
    const name = this.current_token.value as string;
    this.advance();
    this.expect(TokenType.COLON);
    const body = this.parseBlock();
    return ClassDefinition(name, body);
  }

  private parseImportStatement(): Statement {
    if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
      throw new SyntaxError(
        `Expected module name after 'import' at line ${this.current_token?.line}`
      );
    }
    const module = this.current_token.value as string;
    this.advance();
    return ImportStatement(module);
  }

  private parseFromImportStatement(): Statement {
    if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
      throw new SyntaxError(
        `Expected module name after 'from' at line ${this.current_token?.line}`
      );
    }
    const module = this.current_token.value as string;
    this.advance();
    if (!(
      this.current_token &&
      (this.current_token?.type as TokenType) === TokenType.KEYWORD &&
      (this.current_token.value as string) === 'import'
    )) {
      throw new SyntaxError(
        `Expected 'import' after module name at line ${this.current_token?.line}`
      );
    }
    this.advance();
    if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.IDENTIFIER) {
      throw new SyntaxError(
        `Expected name to import at line ${this.current_token?.line}`
      );
    }
    const name = this.current_token.value as string;
    this.advance();
    return FromImportStatement(module, name);
  }

  private parseBlock(): Statement[] {
    const statements: Statement[] = [];
    while (this.current_token && (this.current_token?.type as TokenType) === TokenType.NEWLINE) {
      this.advance();
    }
    if (!this.current_token || (this.current_token?.type as TokenType) !== TokenType.INDENT) {
      // Single-line block
      const stmt = this.parseStatement();
      if (stmt) statements.push(stmt);
      return statements;
    }
    this.advance(); // consume INDENT
    while (
      this.current_token &&
      (this.current_token?.type as TokenType) !== TokenType.DEDENT &&
      (this.current_token?.type as TokenType) !== TokenType.EOF
    ) {
      if ((this.current_token?.type as TokenType) === TokenType.NEWLINE) {
        this.advance();
        continue;
      }
      const stmt = this.parseStatement();
      if (stmt) statements.push(stmt);
      while (this.current_token && (this.current_token?.type as TokenType) === TokenType.NEWLINE) {
        this.advance();
      }
    }
    if (this.current_token && (this.current_token?.type as TokenType) === TokenType.DEDENT) {
      this.advance();
    }
    return statements;
  }
}