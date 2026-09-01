/**
 * TypeScript port of `src/lexer/lexer.py`.
 *
 * Lexer that converts Python-subset source code into a stream of tokens.
 * Emits INDENT / DEDENT tokens based on leading whitespace.
 * Handles implicit line continuation inside (), [], and {} brackets.
 */

export enum TokenType {
  // Literals
  INTEGER = 'INTEGER',
  FLOAT = 'FLOAT',
  STRING = 'STRING',
  IDENTIFIER = 'IDENTIFIER',
  KEYWORD = 'KEYWORD',

  // Operators
  PLUS = 'PLUS',
  MINUS = 'MINUS',
  MULTIPLY = 'MULTIPLY',
  DIVIDE = 'DIVIDE',
  INTEGER_DIVIDE = 'INTEGER_DIVIDE',
  MODULO = 'MODULO',
  EQUAL = 'EQUAL',

  // Augmented assignment
  PLUSEQUAL = 'PLUSEQUAL',
  MINUSEQUAL = 'MINUSEQUAL',
  MULTIPLYEQUAL = 'MULTIPLYEQUAL',
  DIVIDEEQUAL = 'DIVIDEEQUAL',
  INTEGERDIVIDEEQUAL = 'INTEGERDIVIDEEQUAL',
  MODULOEQUAL = 'MODULOEQUAL',

  EQUAL_EQUAL = 'EQUAL_EQUAL',
  NOT_EQUAL = 'NOT_EQUAL',
  LESS = 'LESS',
  GREATER = 'GREATER',
  LESS_EQUAL = 'LESS_EQUAL',
  GREATER_EQUAL = 'GREATER_EQUAL',

  // Punctuation
  LPAREN = 'LPAREN',
  RPAREN = 'RPAREN',
  LBRACKET = 'LBRACKET',
  RBRACKET = 'RBRACKET',
  LBRACE = 'LBRACE',
  RBRACE = 'RBRACE',
  COMMA = 'COMMA',
  COLON = 'COLON',
  SEMICOLON = 'SEMICOLON',
  DOT = 'DOT',

  // Special
  NEWLINE = 'NEWLINE',
  INDENT = 'INDENT',
  DEDENT = 'DEDENT',
  EOF = 'EOF',
  COMMENT = 'COMMENT',
}

export interface Token {
  type: TokenType;
  value: string | number | null;
  line: number;
  column: number;
}

// Python keywords
export const KEYWORDS: Set<string> = new Set([
  'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return',
  'import', 'from', 'as', 'pass', 'break', 'continue', 'in', 'is',
  'and', 'or', 'not', 'True', 'False', 'None', 'try', 'except',
  'finally', 'raise', 'with', 'global', 'nonlocal', 'lambda',
]);

interface TokenSpec {
  type: string;
  regex: RegExp;
}

const buildSpecs = (): TokenSpec[] => [
  { type: 'FLOAT', regex: /^\d+\.\d*/ },
  { type: 'INTEGER', regex: /^\d+/ },
  { type: 'STRING', regex: /^("[^"]*"|'[^']*')/ },
  { type: 'IDENTIFIER', regex: /^[a-zA-Z_][a-zA-Z0-9_]*/ },
  { type: 'EQUAL_EQUAL', regex: /^==/ },
  { type: 'NOT_EQUAL', regex: /^!=/ },
  { type: 'LESS_EQUAL', regex: /^<=/ },
  { type: 'GREATER_EQUAL', regex: /^>=/ },
  // Augmented assignment (must come BEFORE single-char operators)
  { type: 'PLUSEQUAL', regex: /^\+=/ },
  { type: 'MINUSEQUAL', regex: /^-=/ },
  { type: 'MULTIPLYEQUAL', regex: /^\*=/ },
  { type: 'INTEGERDIVIDEEQUAL', regex: /^\/\/=/ },
  { type: 'DIVIDEEQUAL', regex: /^\/=/ },
  { type: 'MODULOEQUAL', regex: /^%=/ },
  { type: 'PLUS', regex: /^\+/ },
  { type: 'MINUS', regex: /^-/ },
  { type: 'MULTIPLY', regex: /^\*/ },
  { type: 'INTEGER_DIVIDE', regex: /^\/\// },
  { type: 'DIVIDE', regex: /^\// },
  { type: 'MODULO', regex: /^%/ },
  { type: 'EQUAL', regex: /^=/ },
  { type: 'LESS', regex: /^</ },
  { type: 'GREATER', regex: /^>/ },
  { type: 'LPAREN', regex: /^\(/ },
  { type: 'RPAREN', regex: /^\)/ },
  { type: 'LBRACKET', regex: /^\[/ },
  { type: 'RBRACKET', regex: /^\]/ },
  { type: 'LBRACE', regex: /^\{/ },
  { type: 'RBRACE', regex: /^\}/ },
  { type: 'COMMA', regex: /^,/ },
  { type: 'COLON', regex: /^:/ },
  { type: 'SEMICOLON', regex: /^;/ },
  { type: 'DOT', regex: /^\./ },
  { type: 'NEWLINE', regex: /^\r?\n/ },
  { type: 'COMMENT', regex: /^#.*/ },
  { type: 'SKIP', regex: /^[ \t\r]+/ },
  { type: 'MISMATCH', regex: /^./ },
];

// Map a string token-type name to the matching TokenType enum value.
const TYPE_NAME_TO_ENUM: Record<string, TokenType> = {
  INTEGER: TokenType.INTEGER,
  FLOAT: TokenType.FLOAT,
  STRING: TokenType.STRING,
  IDENTIFIER: TokenType.IDENTIFIER,
  KEYWORD: TokenType.KEYWORD,
  PLUS: TokenType.PLUS,
  MINUS: TokenType.MINUS,
  MULTIPLY: TokenType.MULTIPLY,
  DIVIDE: TokenType.DIVIDE,
  INTEGER_DIVIDE: TokenType.INTEGER_DIVIDE,
  MODULO: TokenType.MODULO,
  EQUAL: TokenType.EQUAL,
  PLUSEQUAL: TokenType.PLUSEQUAL,
  MINUSEQUAL: TokenType.MINUSEQUAL,
  MULTIPLYEQUAL: TokenType.MULTIPLYEQUAL,
  DIVIDEEQUAL: TokenType.DIVIDEEQUAL,
  INTEGERDIVIDEEQUAL: TokenType.INTEGERDIVIDEEQUAL,
  MODULOEQUAL: TokenType.MODULOEQUAL,
  EQUAL_EQUAL: TokenType.EQUAL_EQUAL,
  NOT_EQUAL: TokenType.NOT_EQUAL,
  LESS: TokenType.LESS,
  GREATER: TokenType.GREATER,
  LESS_EQUAL: TokenType.LESS_EQUAL,
  GREATER_EQUAL: TokenType.GREATER_EQUAL,
  LPAREN: TokenType.LPAREN,
  RPAREN: TokenType.RPAREN,
  LBRACKET: TokenType.LBRACKET,
  RBRACKET: TokenType.RBRACKET,
  LBRACE: TokenType.LBRACE,
  RBRACE: TokenType.RBRACE,
  COMMA: TokenType.COMMA,
  COLON: TokenType.COLON,
  SEMICOLON: TokenType.SEMICOLON,
  DOT: TokenType.DOT,
  NEWLINE: TokenType.NEWLINE,
  INDENT: TokenType.INDENT,
  DEDENT: TokenType.DEDENT,
  EOF: TokenType.EOF,
  COMMENT: TokenType.COMMENT,
};

function getTokenTypeFromString(typeStr: string): TokenType {
  const found = TYPE_NAME_TO_ENUM[typeStr];
  if (!found) throw new Error(`Unknown token type: ${typeStr}`);
  return found;
}

export class Lexer {
  private source: string;
  private tokens: Token[] = [];
  private line = 1;
  private column = 1;
  private pos = 0;
  private specs: TokenSpec[];

  constructor(source: string) {
    this.source = source;
    this.specs = buildSpecs();
  }

  tokenize(): Token[] {
    this.tokens = [];
    this.pos = 0;
    this.line = 1;
    this.column = 1;
    const indentStack: number[] = [0];
    let atLineStart = true;
    let bracketDepth = 0;

    while (this.pos < this.source.length) {
      if (atLineStart && bracketDepth === 0) {
        atLineStart = false;
        // Measure indent
        let indent = 0;
        while (
          this.pos < this.source.length &&
          (this.source[this.pos] === ' ' || this.source[this.pos] === '\t')
        ) {
          if (this.source[this.pos] === '\t') indent += 4;
          else indent += 1;
          this.pos += 1;
          this.column += 1;
        }
        // Skip blank lines and comment-only lines
        if (
          this.pos >= this.source.length ||
          this.source[this.pos] === '\n' ||
          this.source[this.pos] === '#'
        ) {
          // continue to main loop to skip the rest of the line
        } else {
          const top = indentStack[indentStack.length - 1];
          if (indent > top) {
            indentStack.push(indent);
            this.tokens.push({ type: TokenType.INDENT, value: indent, line: this.line, column: this.column });
          } else if (indent < top) {
            while (indentStack.length > 0 && indentStack[indentStack.length - 1] > indent) {
              indentStack.pop();
              this.tokens.push({ type: TokenType.DEDENT, value: indent, line: this.line, column: this.column });
            }
            if (indentStack.length === 0 || indentStack[indentStack.length - 1] !== indent) {
              throw new SyntaxError(
                `Indentation does not match any outer level at line ${this.line}`
              );
            }
          }
        }
      } else if (atLineStart && bracketDepth > 0) {
        atLineStart = false;
        while (
          this.pos < this.source.length &&
          (this.source[this.pos] === ' ' || this.source[this.pos] === '\t')
        ) {
          this.pos += 1;
          this.column += 1;
        }
      }

      if (this.pos >= this.source.length) break;

      // Find a matching token spec
      let matchedType: string | null = null;
      let matchedValue: string | null = null;
      const remaining = this.source.slice(this.pos);
      for (const spec of this.specs) {
        const m = remaining.match(spec.regex);
        if (m && m.index === 0) {
          matchedType = spec.type;
          matchedValue = m[0];
          break;
        }
      }
      if (matchedType === null || matchedValue === null) {
        throw new SyntaxError(
          `Illegal character at line ${this.line}, column ${this.column}: '${this.source[this.pos]}'`
        );
      }

      let token: Token | null = null;

      if (matchedType === 'INTEGER') {
        token = { type: TokenType.INTEGER, value: parseInt(matchedValue, 10), line: this.line, column: this.column };
      } else if (matchedType === 'FLOAT') {
        token = { type: TokenType.FLOAT, value: parseFloat(matchedValue), line: this.line, column: this.column };
      } else if (matchedType === 'STRING') {
        token = { type: TokenType.STRING, value: matchedValue.slice(1, -1), line: this.line, column: this.column };
      } else if (matchedType === 'IDENTIFIER') {
        if (KEYWORDS.has(matchedValue)) {
          token = { type: TokenType.KEYWORD, value: matchedValue, line: this.line, column: this.column };
        } else {
          token = { type: TokenType.IDENTIFIER, value: matchedValue, line: this.line, column: this.column };
        }
      } else if (matchedType === 'NEWLINE') {
        if (bracketDepth === 0) {
          token = { type: TokenType.NEWLINE, value: matchedValue, line: this.line, column: this.column };
        }
        this.line += 1;
        this.column = 1;
        atLineStart = true;
      } else if (matchedType === 'SKIP') {
        token = null;
      } else if (matchedType === 'COMMENT') {
        token = null;
      } else if (matchedType === 'MISMATCH') {
        throw new SyntaxError(
          `Illegal character at line ${this.line}, column ${this.column}: '${matchedValue}'`
        );
      } else {
        const tokenTypeEnum = getTokenTypeFromString(matchedType);
        token = { type: tokenTypeEnum, value: matchedValue, line: this.line, column: this.column };
      }

      // Track bracket depth
      if (matchedType === 'LPAREN' || matchedType === 'LBRACKET' || matchedType === 'LBRACE') {
        bracketDepth += 1;
      } else if (matchedType === 'RPAREN' || matchedType === 'RBRACKET' || matchedType === 'RBRACE') {
        bracketDepth -= 1;
        if (bracketDepth < 0) {
          throw new SyntaxError(`Unmatched closing bracket '${matchedValue}' at line ${this.line}`);
        }
      }

      if (token !== null) {
        this.tokens.push(token);
      }

      this.pos += matchedValue.length;
      this.column += matchedValue.length;
    }

    // Flush remaining DEDENTs
    while (indentStack.length > 1) {
      indentStack.pop();
      this.tokens.push({ type: TokenType.DEDENT, value: 0, line: this.line, column: this.column });
    }

    this.tokens.push({ type: TokenType.EOF, value: '', line: this.line, column: this.column });
    return this.tokens;
  }
}