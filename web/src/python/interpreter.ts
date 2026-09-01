/**
 * TypeScript port of `src/interpreter/interpreter.py`.
 *
 * Tree-walking interpreter for the Python-subset AST.
 */

import { TokenType } from './lexer';
import {
  ASTNode, Expression, Statement,
  ProgramNode,
  BinaryExpressionNode, UnaryExpressionNode, AssignmentExpressionNode,
  FunctionCallNode, SubscriptExpressionNode, AttributeAccessNode, MethodCallNode,
  ListLiteralNode, TupleLiteralNode, DictLiteralNode, SetLiteralNode,
  ExpressionStatementNode, FunctionDefinitionNode, IfStatementNode,
  ForStatementNode, WhileStatementNode, ReturnStatementNode,
  BreakStatementNode, ContinueStatementNode, ClassDefinitionNode,
  ImportStatementNode, FromImportStatementNode, BlockNode,
} from './ast';

// === Control-flow signals ===

export class ReturnSignal {
  constructor(public value: unknown) {}
}
export class BreakSignal {}
export class ContinueSignal {}

// === Output writer interface ===

export interface OutputWriter {
  stdout(text: string): void;
  stderr(text: string): void;
}

// === Custom errors ===

export class RuntimeError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RuntimeError';
  }
}

export class NameErrorType extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NameError';
  }
}

export class TypeErrorPy extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'TypeError';
  }
}

export class IndexErrorPy extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'IndexError';
  }
}

export class KeyErrorPy extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'KeyError';
  }
}

export class AttributeErrorPy extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AttributeError';
  }
}

// === Helpers ===

export function formatValue(obj: unknown): string {
  if (obj === null || obj === undefined) return 'None';
  if (typeof obj === 'boolean') return obj ? 'True' : 'False';
  if (typeof obj === 'string') return obj;
  if (typeof obj === 'number') {
    return obj.toString();
  }
  if (Array.isArray(obj)) {
    return '[' + obj.map(formatValue).join(', ') + ']';
  }
  if (obj instanceof Map) {
    const pairs: string[] = [];
    obj.forEach((v, k) => {
      pairs.push(formatValue(k) + ': ' + formatValue(v));
    });
    return '{' + pairs.join(', ') + '}';
  }
  if (obj instanceof Set) {
    return '{' + Array.from(obj).map(formatValue).join(', ') + '}';
  }
  if (typeof obj === 'function') {
    const fn = obj as any;
    if (fn.__pyfunc__) return `<function ${fn.__name__}>`;
    return '<built-in function>';
  }
  if (typeof obj === 'object') {
    const o = obj as any;
    if (o.__pytuple__) {
      return '(' + o.__items__.map(formatValue).join(', ') + (o.__items__.length === 1 ? ',' : '') + ')';
    }
    if (o.__pyname__) return `<class '${o.__pyname__}'>`;
    return String(obj);
  }
  return String(obj);
}

function toArray(obj: unknown): unknown[] {
  if (obj === null || obj === undefined) return [];
  if (Array.isArray(obj)) return obj.slice();
  if (obj instanceof Set) return Array.from(obj);
  if (obj instanceof Map) return Array.from(obj.keys());
  if (typeof obj === 'object' && obj !== null && (obj as any).__pytuple__) {
    return ((obj as any).__items__ as unknown[]).slice();
  }
  if (typeof obj === 'string') return Array.from(obj);
  throw new RuntimeError(`object is not iterable`);
}

function iter(obj: unknown): Iterable<unknown> {
  if (obj === null || obj === undefined) return [];
  if (Array.isArray(obj)) return obj;
  if (obj instanceof Set) return obj.values();
  if (obj instanceof Map) return obj.keys();
  if (typeof obj === 'object' && obj !== null && (obj as any).__pytuple__) {
    return (obj as any).__items__;
  }
  if (typeof obj === 'string') return obj;
  throw new RuntimeError(`object is not iterable`);
}

function isTruthy(value: unknown): boolean {
  return Boolean(value);
}

// === Built-in functions ===

const _print = (args: unknown[], out: OutputWriter): void => {
  out.stdout(args.map(formatValue).join(' ') + '\n');
};

const _len = (obj: unknown): number => {
  if (obj === null || obj === undefined) {
    throw new RuntimeError(`object of type '${typeof obj}' has no len()`);
  }
  if (typeof obj === 'string' || Array.isArray(obj)) return (obj as any).length;
  if (obj instanceof Set) return obj.size;
  if (obj instanceof Map) return obj.size;
  if (typeof obj === 'object' && (obj as any).__pytuple__) {
    return ((obj as any).__items__ as unknown[]).length;
  }
  throw new RuntimeError(`object has no len()`);
};

const _range = (...args: number[]): number[] => {
  if (args.length === 1) {
    const stop = args[0];
    const result: number[] = [];
    for (let i = 0; i < stop; i++) result.push(i);
    return result;
  }
  if (args.length === 2) {
    const [start, stop] = args;
    const result: number[] = [];
    for (let i = start; i < stop; i++) result.push(i);
    return result;
  }
  if (args.length === 3) {
    const [start, stop, step] = args;
    const result: number[] = [];
    if (step === 0) throw new RuntimeError('range() arg 3 must not be zero');
    if (step > 0) {
      for (let i = start; i < stop; i += step) result.push(i);
    } else {
      for (let i = start; i > stop; i += step) result.push(i);
    }
    return result;
  }
  throw new RuntimeError(`range expected at most 3 arguments, got ${args.length}`);
};

const _str = (obj: unknown): string => formatValue(obj);

const _int = (obj: unknown): number => {
  if (typeof obj === 'number') return Math.trunc(obj);
  if (typeof obj === 'string') {
    const n = parseInt(obj, 10);
    if (Number.isNaN(n)) throw new RuntimeError(`int() invalid literal: '${obj}'`);
    return n;
  }
  if (typeof obj === 'boolean') return obj ? 1 : 0;
  throw new RuntimeError(`int() argument must be string, number, or boolean`);
};

const _float = (obj: unknown): number => {
  if (typeof obj === 'number') return obj;
  if (typeof obj === 'string') {
    const n = parseFloat(obj);
    if (Number.isNaN(n)) throw new RuntimeError(`float() invalid literal: '${obj}'`);
    return n;
  }
  if (typeof obj === 'boolean') return obj ? 1.0 : 0.0;
  throw new RuntimeError(`float() argument must be string, number, or boolean`);
};

const _bool = (obj: unknown): boolean => {
  if (obj === undefined || obj === null) return false;
  if (typeof obj === 'boolean') return obj;
  if (typeof obj === 'number') return obj !== 0;
  if (typeof obj === 'string') return obj.length > 0;
  if (Array.isArray(obj)) return obj.length > 0;
  if (obj instanceof Set || obj instanceof Map) return obj.size > 0;
  if (typeof obj === 'object' && (obj as any).__pytuple__) {
    return ((obj as any).__items__ as unknown[]).length > 0;
  }
  return true;
};

const _list = (obj: unknown): unknown[] => {
  if (obj === null || obj === undefined) return [];
  if (Array.isArray(obj)) return obj.slice();
  return toArray(obj);
};

const _tuple = (obj: unknown): PyTuple => {
  return makeTuple(toArray(obj));
};

const _set = (obj: unknown): Set<unknown> => {
  if (obj === null || obj === undefined) return new Set();
  if (obj instanceof Set) return new Set(obj);
  return new Set(toArray(obj));
};

const _dict = (obj: unknown): Map<unknown, unknown> => {
  if (obj === null || obj === undefined) return new Map();
  if (obj instanceof Map) return new Map(obj);
  if (Array.isArray(obj)) {
    const m = new Map<unknown, unknown>();
    for (const pair of obj) {
      if (!Array.isArray(pair) || pair.length !== 2) {
        throw new RuntimeError(`dict() elements must be key/value pairs`);
      }
      m.set(pair[0], pair[1]);
    }
    return m;
  }
  throw new RuntimeError(`dict() argument must be a mapping or iterable of pairs`);
};

const _type = (obj: unknown): string => {
  if (obj === null) return 'NoneType';
  if (obj === undefined) return 'NoneType';
  if (typeof obj === 'boolean') return 'bool';
  if (typeof obj === 'number') return Number.isInteger(obj) ? 'int' : 'float';
  if (typeof obj === 'string') return 'str';
  if (Array.isArray(obj)) return 'list';
  if (obj instanceof Map) return 'dict';
  if (obj instanceof Set) return 'set';
  if (typeof obj === 'function') {
    const fn = obj as any;
    if (fn.__pyfunc__) return 'function';
    return 'builtin_function_or_method';
  }
  if (typeof obj === 'object') {
    const o = obj as any;
    if (o.__pytuple__) return 'tuple';
    if (o.__pyname__) return 'class';
    return 'object';
  }
  return typeof obj;
};

const _sorted = (obj: unknown): unknown[] => {
  const list = toArray(obj);
  return [...list].sort((a, b) => {
    if (typeof a === 'number' && typeof b === 'number') return (a as number) - (b as number);
    return String(a) < String(b) ? -1 : String(a) > String(b) ? 1 : 0;
  });
};

const _sum = (obj: unknown): number => {
  let total = 0;
  for (const v of iter(obj)) total += Number(v);
  return total;
};

const _min = (...args: unknown[]): unknown => {
  if (args.length === 1) {
    const list = toArray(args[0]);
    if (list.length === 0) throw new RuntimeError('min() arg is an empty sequence');
    return list.reduce((a, b) => ((a as any) <= (b as any) ? a : b));
  }
  if (args.length === 0) throw new RuntimeError('min() expected at least 1 argument, got 0');
  return args.reduce((a, b) => ((a as any) <= (b as any) ? a : b));
};

const _max = (...args: unknown[]): unknown => {
  if (args.length === 1) {
    const list = toArray(args[0]);
    if (list.length === 0) throw new RuntimeError('max() arg is an empty sequence');
    return list.reduce((a, b) => ((a as any) >= (b as any) ? a : b));
  }
  if (args.length === 0) throw new RuntimeError('max() expected at least 1 argument, got 0');
  return args.reduce((a, b) => ((a as any) >= (b as any) ? a : b));
};

const _abs = (obj: unknown): number => Math.abs(Number(obj));

const _ord = (obj: unknown): number => {
  if (typeof obj !== 'string' || obj.length !== 1) {
    throw new RuntimeError(`ord() expected a character, got ${formatValue(obj)}`);
  }
  return obj.charCodeAt(0);
};

const _chr = (obj: unknown): string => {
  const n = Number(obj);
  if (!Number.isInteger(n) || n < 0 || n > 0x10ffff) {
    throw new RuntimeError(`chr() arg not in range(0x110000)`);
  }
  return String.fromCodePoint(n);
};

// === Tuple wrapper ===

export interface PyTuple {
  __pytuple__: true;
  __items__: unknown[];
}

export function makeTuple(items: unknown[]): PyTuple {
  return { __pytuple__: true, __items__: items };
}

// === User-defined function ===

export interface PyFunction {
  __pyfunc__: true;
  __name__: string;
  parameters: string[];
  body: Statement[];
  closure: Record<string, unknown>;
}

export function makePyFunction(
  name: string,
  parameters: string[],
  body: Statement[],
  closure: Record<string, unknown>
): PyFunction {
  return {
    __pyfunc__: true,
    __name__: name,
    parameters,
    body,
    closure,
  };
}

// === Main Interpreter class ===

export interface BuiltinFunction {
  __pybuiltin__: true;
  name: string;
  fn: (args: unknown[], out: OutputWriter) => unknown;
}

function makeBuiltin(name: string, fn: BuiltinFunction['fn']): BuiltinFunction {
  return { __pybuiltin__: true, name, fn };
}

export class Interpreter {
  private globalScope: Record<string, unknown> = {};
  private scopeStack: Record<string, unknown>[];
  private output: OutputWriter;

  constructor(output: OutputWriter) {
    this.output = output;
    this.globalScope = {};
    this.scopeStack = [this.globalScope];
    this.registerBuiltins();
  }

  // Scope helpers
  pushScope(scope: Record<string, unknown>): void {
    this.scopeStack.push(scope);
  }

  popScope(): Record<string, unknown> {
    return this.scopeStack.pop() as Record<string, unknown>;
  }

  get currentScope(): Record<string, unknown> {
    return this.scopeStack[this.scopeStack.length - 1];
  }

  private registerBuiltins(): void {
    const builtins: Record<string, BuiltinFunction> = {
      print: makeBuiltin('print', (args) => { _print(args, this.output); return null; }),
      len: makeBuiltin('len', (args) => _len(args[0])),
      range: makeBuiltin('range', (args) => _range(...(args as number[]))),
      str: makeBuiltin('str', (args) => _str(args[0])),
      int: makeBuiltin('int', (args) => _int(args[0])),
      float: makeBuiltin('float', (args) => _float(args[0])),
      type: makeBuiltin('type', (args) => _type(args[0])),
      sorted: makeBuiltin('sorted', (args) => _sorted(args[0])),
      sum: makeBuiltin('sum', (args) => _sum(args[0])),
      min: makeBuiltin('min', (args) => _min(...args)),
      max: makeBuiltin('max', (args) => _max(...args)),
      abs: makeBuiltin('abs', (args) => _abs(args[0])),
      ord: makeBuiltin('ord', (args) => _ord(args[0])),
      chr: makeBuiltin('chr', (args) => _chr(args[0])),
    };
    for (const [name, fn] of Object.entries(builtins)) {
      this.globalScope[name] = fn;
    }
    // Built-in types
    this.globalScope['int'] = makeBuiltin('int', (args) => _int(args[0]));
    this.globalScope['float'] = makeBuiltin('float', (args) => _float(args[0]));
    this.globalScope['str'] = makeBuiltin('str', (args) => _str(args[0]));
    this.globalScope['bool'] = makeBuiltin('bool', (args) => _bool(args[0]));
    this.globalScope['list'] = makeBuiltin('list', (args) => _list(args[0]));
    this.globalScope['dict'] = makeBuiltin('dict', (args) => _dict(args[0]));
    this.globalScope['tuple'] = makeBuiltin('tuple', (args) => _tuple(args[0]));
    this.globalScope['set'] = makeBuiltin('set', (args) => _set(args[0]));
    this.globalScope['NoneType'] = null;
  }

  interpret(program: ProgramNode): void {
    if (program.kind !== 'Program') {
      throw new RuntimeError(`interpret expected Program, got ${program.kind}`);
    }
    try {
      for (const stmt of program.statements) {
        this.execute(stmt);
      }
    } catch (e) {
      if (e instanceof BreakSignal) {
        throw new RuntimeError(`'break' outside loop`);
      } else if (e instanceof ContinueSignal) {
        throw new RuntimeError(`'continue' not properly in loop`);
      }
      throw e;
    }
  }

  execute(node: ASTNode): unknown {
    const visitor = (this as any)[`visit_${node.kind}`];
    if (!visitor) {
      throw new RuntimeError(`No visitor for AST node type: ${node.kind}`);
    }
    return visitor.call(this, node);
  }

  // === Visitors ===

  visit_Variable(node: { kind: 'Variable'; name: string }): unknown {
    const name = node.name;
    for (let i = this.scopeStack.length - 1; i >= 0; i--) {
      const scope = this.scopeStack[i];
      if (Object.prototype.hasOwnProperty.call(scope, name)) {
        return scope[name];
      }
    }
    throw new NameErrorType(`Name '${name}' is not defined`);
  }

  visit_AssignmentExpression(node: AssignmentExpressionNode): unknown {
    const value = this.execute(node.value);
    if (node.target.kind === 'SubscriptExpression') {
      const sub = node.target as SubscriptExpressionNode;
      const targetObj = this.execute(sub.target);
      const index = this.execute(sub.index);
      if (Array.isArray(targetObj)) {
        if (typeof index !== 'number' || !Number.isInteger(index)) {
          throw new TypeErrorPy('list index must be an integer');
        }
        let idx = index as number;
        if (idx < 0) idx += targetObj.length;
        targetObj[idx] = value;
        return value;
      }
      if (targetObj instanceof Map && !(targetObj as any).__pyname__) {
        targetObj.set(index, value);
        return value;
      }
      throw new TypeErrorPy(
        `'${_type(targetObj)}' object does not support item assignment`
      );
    }
    if (node.target.kind !== 'Variable') {
      throw new RuntimeError('Assignment target must be a variable or subscript');
    }
    const name = (node.target as any).name;
    for (let i = this.scopeStack.length - 1; i >= 0; i--) {
      const scope = this.scopeStack[i];
      if (Object.prototype.hasOwnProperty.call(scope, name)) {
        scope[name] = value;
        return value;
      }
    }
    this.currentScope[name] = value;
    return value;
  }

  visit_Integer(node: { kind: 'Integer'; value: number }): number {
    return node.value;
  }
  visit_Float(node: { kind: 'Float'; value: number }): number {
    return node.value;
  }
  visit_String(node: { kind: 'String'; value: string }): string {
    return node.value;
  }
  visit_Boolean(node: { kind: 'Boolean'; value: boolean }): boolean {
    return node.value;
  }
  visit_NoneLiteral(_node: { kind: 'NoneLiteral' }): null {
    return null;
  }

  visit_BinaryExpression(node: BinaryExpressionNode): unknown {
    // Short-circuit logical operators
    if (node.operator === TokenType.KEYWORD && (node.operator_value === 'and' || node.operator_value === 'or')) {
      const left = this.execute(node.left);
      if (node.operator_value === 'and') {
        if (!isTruthy(left)) return left;
        return this.execute(node.right);
      }
      if (isTruthy(left)) return left;
      return this.execute(node.right);
    }
    // Membership operator: `x in container`, `x not in container`
    if (node.operator === TokenType.KEYWORD && (node.operator_value === 'in' || node.operator_value === 'not in')) {
      const left = this.execute(node.left);
      const right = this.execute(node.right);
      let contained = false;
      if (right === null || right === undefined) {
        contained = false;
      } else if (typeof right === 'string') {
        contained = typeof left === 'string' ? (right as string).includes(left as string) : false;
      } else if (Array.isArray(right)) {
        contained = (right as unknown[]).includes(left);
      } else if (right instanceof Set) {
        contained = right.has(left);
      } else if (right instanceof Map) {
        contained = right.has(left);
      } else if (typeof right === 'object' && (right as any).__pytuple__) {
        contained = ((right as any).__items__ as unknown[]).includes(left);
      } else {
        throw new RuntimeError(
          `argument of type '${_type(right)}' is not iterable`
        );
      }
      return node.operator_value === 'not in' ? !contained : contained;
    }
    // Identity: `x is y`
    if (node.operator === TokenType.KEYWORD && node.operator_value === 'is') {
      const left = this.execute(node.left);
      const right = this.execute(node.right);
      return left === right;
    }

    const left = this.execute(node.left);
    const right = this.execute(node.right);
    const op = node.operator;

    try {
      switch (op) {
        case TokenType.PLUS:
          if (typeof left === 'string' && typeof right === 'string') return left + right;
          if (Array.isArray(left) && Array.isArray(right)) return left.concat(right);
          const leftTup = (typeof left === 'object' && left !== null && (left as any).__pytuple__)
            ? (left as PyTuple).__items__ : null;
          const rightTup = (typeof right === 'object' && right !== null && (right as any).__pytuple__)
            ? (right as PyTuple).__items__ : null;
          if (leftTup && rightTup) return makeTuple(leftTup.concat(rightTup));
          if (leftTup && Array.isArray(right)) return makeTuple(leftTup.concat(right));
          if (Array.isArray(left) && rightTup) return makeTuple(left.concat(rightTup));
          return (left as any) + (right as any);
        case TokenType.MINUS: return (left as any) - (right as any);
        case TokenType.MULTIPLY: return (left as any) * (right as any);
        case TokenType.DIVIDE:
          if (right === 0) throw new RuntimeError('Division by zero');
          return (left as any) / (right as any);
        case TokenType.INTEGER_DIVIDE:
          if (right === 0) throw new RuntimeError('Division by zero');
          return Math.floor((left as any) / (right as any));
        case TokenType.MODULO:
          if (right === 0) throw new RuntimeError('Modulo by zero');
          return (left as any) % (right as any);
        case TokenType.EQUAL_EQUAL: return left === right;
        case TokenType.NOT_EQUAL: return left !== right;
        case TokenType.LESS: return (left as any) < (right as any);
        case TokenType.GREATER: return (left as any) > (right as any);
        case TokenType.LESS_EQUAL: return (left as any) <= (right as any);
        case TokenType.GREATER_EQUAL: return (left as any) >= (right as any);
        default:
          throw new RuntimeError(`Unsupported binary operator: ${op}`);
      }
    } catch (e) {
      if (e instanceof RuntimeError) throw e;
      throw new RuntimeError(`Type error in binary op ${op}: ${(e as Error).message}`);
    }
  }

  visit_UnaryExpression(node: UnaryExpressionNode): unknown {
    const operand = this.execute(node.operand);
    const op = node.operator;
    if (op === TokenType.MINUS) return -(operand as any);
    if (op === TokenType.PLUS) return +(operand as any);
    if (op === TokenType.KEYWORD && node.operator_value === 'not') return !isTruthy(operand);
    throw new RuntimeError(`Unsupported unary operator: ${op}`);
  }

  visit_ListLiteral(node: ListLiteralNode): unknown[] {
    return node.elements.map((e) => this.execute(e));
  }

  visit_TupleLiteral(node: TupleLiteralNode): PyTuple {
    return makeTuple(node.elements.map((e) => this.execute(e)));
  }

  visit_DictLiteral(node: DictLiteralNode): Map<unknown, unknown> {
    const m = new Map<unknown, unknown>();
    for (const [k, v] of node.entries) {
      m.set(this.execute(k), this.execute(v));
    }
    return m;
  }

  visit_SetLiteral(node: SetLiteralNode): Set<unknown> {
    const s = new Set<unknown>();
    for (const el of node.elements) s.add(this.execute(el));
    return s;
  }

  visit_SubscriptExpression(node: SubscriptExpressionNode): unknown {
    const target = this.execute(node.target);
    const index = this.execute(node.index);
    if (typeof target === 'string') {
      if (typeof index !== 'number' || !Number.isInteger(index)) {
        throw new TypeErrorPy('string index must be an integer');
      }
      let i = index as number;
      if (i < 0) i += (target as string).length;
      if (i < 0 || i >= (target as string).length) {
        throw new IndexErrorPy(`string index out of range: ${index}`);
      }
      return (target as string)[i];
    }
    if (Array.isArray(target)) {
      if (typeof index !== 'number' || !Number.isInteger(index)) {
        throw new TypeErrorPy(`List indices must be integers, not ${_type(index)}`);
      }
      let i = index as number;
      if (i < 0) i += (target as unknown[]).length;
      if (i < 0 || i >= (target as unknown[]).length) {
        throw new IndexErrorPy(`list index out of range: ${index}`);
      }
      return (target as unknown[])[i];
    }
    if (typeof target === 'object' && target !== null && (target as any).__pytuple__) {
      if (typeof index !== 'number' || !Number.isInteger(index)) {
        throw new TypeErrorPy(`Tuple indices must be integers, not ${_type(index)}`);
      }
      const items = (target as PyTuple).__items__;
      let i = index as number;
      if (i < 0) i += items.length;
      if (i < 0 || i >= items.length) {
        throw new IndexErrorPy(`tuple index out of range: ${index}`);
      }
      return items[i];
    }
    if (target instanceof Map && !(target as any).__pyname__) {
      if (!target.has(index)) {
        throw new KeyErrorPy(`${formatValue(index)}`);
      }
      return target.get(index);
    }
    throw new TypeErrorPy(`'${_type(target)}' object is not subscriptable`);
  }

  visit_AttributeAccess(node: AttributeAccessNode): unknown {
    const target = this.execute(node.target);
    return this._lookupAttr(target, node.attribute);
  }

  private _lookupAttr(target: unknown, name: string): unknown {
    // class instance: __dict__
    if (typeof target === 'object' && target !== null && (target as any).__pyclass__) {
      const inst = target as any;
      if (Object.prototype.hasOwnProperty.call(inst.__dict__, name)) {
        return inst.__dict__[name];
      }
      // Methods
      const klass = inst.__pyname__ ? this.globalScope[inst.__pyname__] : null;
      if (klass && typeof klass === 'object' && (klass as any).__pyname__) {
        const methods = (klass as any).methods;
        if (methods && Object.prototype.hasOwnProperty.call(methods, name)) {
          return this._bindMethod(target, methods[name], klass);
        }
      }
      throw new AttributeErrorPy(
        `'${(inst as any).__pyname__}' object has no attribute '${name}'`
      );
    }
    // Built-in methods on strings/lists/etc
    if (typeof target === 'string') {
      return this._stringAttr(target as string, name);
    }
    if (Array.isArray(target)) {
      return this._listAttr(target, name);
    }
    if (target instanceof Map) {
      return this._dictAttr(target, name);
    }
    if (target instanceof Set) {
      return this._setAttr(target, name);
    }
    if (typeof target === 'object' && target !== null && (target as any).__pytuple__) {
      return this._tupleAttr(target as PyTuple, name);
    }
    throw new AttributeErrorPy(`'${_type(target)}' object has no attribute '${name}'`);
  }

  // === Built-in attribute accessors (return callable functions) ===

  private _stringAttr(self: string, name: string): BuiltinFunction {
    switch (name) {
      case 'upper': return makeBuiltin('upper', () => self.toUpperCase());
      case 'lower': return makeBuiltin('lower', () => self.toLowerCase());
      case 'strip': return makeBuiltin('strip', () => self.trim());
      case 'split': return makeBuiltin('split', (args) => self.split(String(args[0] ?? ' ')));
      case 'startswith': return makeBuiltin('startswith', (args) => self.startsWith(String(args[0])));
      case 'endswith': return makeBuiltin('endswith', (args) => self.endsWith(String(args[0])));
      case 'replace': return makeBuiltin('replace', (args) =>
        self.replace(String(args[0]), String(args[1]))
      );
      case 'join': return makeBuiltin('join', (args) => {
        const items = toArray(args[0]);
        return items.map(String).join(self);
      });
      case 'find': return makeBuiltin('find', (args) => self.indexOf(String(args[0])));
      case 'count': return makeBuiltin('count', (args) => {
        const s = String(args[0]);
        let count = 0;
        let pos = 0;
        while ((pos = self.indexOf(s, pos)) !== -1) { count++; pos += s.length; }
        return count;
      });
      case 'isdigit': return makeBuiltin('isdigit', () => /^\d+$/.test(self));
      case 'isalpha': return makeBuiltin('isalpha', () => /^[a-zA-Z]+$/.test(self));
      case 'format': return makeBuiltin('format', () => self);
      default: throw new AttributeErrorPy(`'str' object has no attribute '${name}'`);
    }
  }

  private _listAttr(self: unknown[], name: string): BuiltinFunction {
    switch (name) {
      case 'append': return makeBuiltin('append', (args) => { self.push(args[0]); return null; });
      case 'extend': return makeBuiltin('extend', (args) => {
        for (const v of iter(args[0])) self.push(v);
        return null;
      });
      case 'insert': return makeBuiltin('insert', (args) => {
        self.splice(Number(args[0]), 0, args[1]);
        return null;
      });
      case 'remove': return makeBuiltin('remove', (args) => {
        const i = self.indexOf(args[0]);
        if (i === -1) throw new RuntimeError(`list.remove(x): x not in list`);
        self.splice(i, 1);
        return null;
      });
      case 'pop': return makeBuiltin('pop', (args) => {
        if (args.length === 0) return self.pop();
        const i = Number(args[0]);
        return self.splice(i, 1)[0];
      });
      case 'clear': return makeBuiltin('clear', () => { self.length = 0; return null; });
      case 'sort': return makeBuiltin('sort', () => { self.sort(); return null; });
      case 'reverse': return makeBuiltin('reverse', () => { self.reverse(); return null; });
      case 'index': return makeBuiltin('index', (args) => {
        const i = self.indexOf(args[0]);
        if (i === -1) throw new RuntimeError(`${formatValue(args[0])} is not in list`);
        return i;
      });
      case 'count': return makeBuiltin('count', (args) => self.filter((v) => v === args[0]).length);
      case 'copy': return makeBuiltin('copy', () => [...self]);
      default: throw new AttributeErrorPy(`'list' object has no attribute '${name}'`);
    }
  }
  private _dictAttr(self: Map<unknown, unknown>, name: string): BuiltinFunction {
    switch (name) {
      case 'get': return makeBuiltin('get', (args) => self.get(args[0]));
      case 'keys': return makeBuiltin('keys', () => Array.from(self.keys()));
      case 'values': return makeBuiltin('values', () => Array.from(self.values()));
      case 'items': return makeBuiltin('items', () => Array.from(self.entries()));
      case 'pop': return makeBuiltin('pop', (args) => {
        if (!self.has(args[0])) throw new KeyErrorPy(`${formatValue(args[0])}`);
        const v = self.get(args[0]);
        self.delete(args[0]);
        return v;
      });
      case 'clear': return makeBuiltin('clear', () => { self.clear(); return null; });
      case 'update': return makeBuiltin('update', (args) => {
        const other = args[0];
        if (other instanceof Map) other.forEach((v, k) => self.set(k, v));
        else throw new TypeErrorPy('update requires dict');
        return null;
      });
      case 'setdefault': return makeBuiltin('setdefault', (args) => {
        if (!self.has(args[0])) self.set(args[0], args[1] ?? null);
        return self.get(args[0]);
      });
      case 'copy': return makeBuiltin('copy', () => new Map(self));
      default: throw new AttributeErrorPy(`'dict' object has no attribute '${name}'`);
    }
  }

  private _setAttr(self: Set<unknown>, name: string): BuiltinFunction {
    switch (name) {
      case 'add': return makeBuiltin('add', (args) => { self.add(args[0]); return null; });
      case 'remove': return makeBuiltin('remove', (args) => {
        if (!self.has(args[0])) throw new KeyErrorPy(`${formatValue(args[0])}`);
        self.delete(args[0]);
        return null;
      });
      case 'discard': return makeBuiltin('discard', (args) => { self.delete(args[0]); return null; });
      case 'clear': return makeBuiltin('clear', () => { self.clear(); return null; });
      case 'pop': return makeBuiltin('pop', () => {
        const v = self.values().next().value;
        if (v === undefined) throw new RuntimeError('pop from an empty set');
        self.delete(v);
        return v;
      });
      case 'union': return makeBuiltin('union', (args) => {
        const s = new Set(self);
        for (const v of iter(args[0])) s.add(v);
        return s;
      });
      case 'intersection': return makeBuiltin('intersection', (args) => {
        const s = new Set<unknown>();
        const other = args[0] instanceof Set ? args[0] : new Set(iter(args[0]));
        for (const v of self) if (other.has(v)) s.add(v);
        return s;
      });
      case 'copy': return makeBuiltin('copy', () => new Set(self));
      default: throw new AttributeErrorPy(`'set' object has no attribute '${name}'`);
    }
  }

  private _tupleAttr(self: PyTuple, name: string): BuiltinFunction {
    switch (name) {
      case 'count': return makeBuiltin('count', (args) =>
        self.__items__.filter((v) => v === args[0]).length
      );
      case 'index': return makeBuiltin('index', (args) => {
        const i = self.__items__.indexOf(args[0]);
        if (i === -1) throw new RuntimeError(`tuple.index(x): x not in tuple`);
        return i;
      });
      default: throw new AttributeErrorPy(`'tuple' object has no attribute '${name}'`);
    }
  }

  private _bindMethod(self: unknown, method: PyFunction, klass: unknown): PyFunction {
    const bound = { ...method };
    const closure = { ...method.closure, self };
    return makePyFunction(method.__name__, method.parameters, method.body, closure);
  }

  visit_FunctionCall(node: FunctionCallNode): unknown {
    const callee = this.execute(node.func);
    const args = node.args.map((a) => this.execute(a));
    return this._callValue(callee, args);
  }

  visit_MethodCall(node: MethodCallNode): unknown {
    const target = this.execute(node.target);
    const method = this._lookupAttr(target, node.method);
    const args = node.args.map((a) => this.execute(a));
    return this._callValue(method, args);
  }

  private _callValue(callee: unknown, args: unknown[]): unknown {
    if (typeof callee === 'object' && callee !== null && (callee as any).__pybuiltin__) {
      return (callee as unknown as BuiltinFunction).fn(args, this.output);
    }
    if (typeof callee === 'function' && (callee as any).__pybuiltin__) {
      return (callee as unknown as BuiltinFunction).fn(args, this.output);
    }
    if (typeof callee === 'object' && callee !== null && (callee as any).__pyfunc__) {
      const fn = callee as unknown as PyFunction;
      if (args.length !== fn.parameters.length) {
        throw new RuntimeError(
          `Function '${fn.__name__}' expected ${fn.parameters.length} argument(s) but got ${args.length}`
        );
      }
      const localScope: Record<string, unknown> = { ...fn.closure };
      for (let i = 0; i < fn.parameters.length; i++) {
        localScope[fn.parameters[i]] = args[i];
      }
      this.pushScope(localScope);
      try {
        for (const stmt of fn.body) {
          this.execute(stmt);
        }
        return null;
      } catch (e) {
        if (e instanceof ReturnSignal) return e.value;
        throw e;
      } finally {
        this.popScope();
      }
    }
    if (typeof callee === 'function' && (callee as any).__pyfunc__) {
      const fn = callee as unknown as PyFunction;
      if (args.length !== fn.parameters.length) {
        throw new RuntimeError(
          `Function '${fn.__name__}' expected ${fn.parameters.length} argument(s) but got ${args.length}`
        );
      }
      const localScope: Record<string, unknown> = { ...fn.closure };
      for (let i = 0; i < fn.parameters.length; i++) {
        localScope[fn.parameters[i]] = args[i];
      }
      this.pushScope(localScope);
      try {
        for (const stmt of fn.body) {
          this.execute(stmt);
        }
        return null;
      } catch (e) {
        if (e instanceof ReturnSignal) return e.value;
        throw e;
      } finally {
        this.popScope();
      }
    }
    if (typeof callee === 'function') {
      return (callee as any)(args);
    }
    if (typeof callee === 'object' && callee !== null && (callee as any).__pyname__) {
      return this._constructClass(callee, args);
    }
    throw new TypeErrorPy(`'${_type(callee)}' object is not callable`);
  }

  private _constructClass(klass: any, args: unknown[]): unknown {
    let initFn: PyFunction | null = null;
    let current: any = klass;
    while (current) {
      if (current.methods && current.methods.__init__) {
        initFn = current.methods.__init__;
        break;
      }
      current = current.__parent__ ? this.globalScope[current.__parent__] : null;
    }
    const instance: any = {
      __pyclass__: true,
      __pyname__: klass.__pyname__,
      __dict__: {},
    };
    if (initFn) {
      const localScope: Record<string, unknown> = { ...initFn.closure, self: instance };
      for (let i = 0; i < initFn.parameters.length; i++) {
        const param = initFn.parameters[i];
        if (i < args.length) {
          localScope[param] = args[i];
        } else if (param === 'self') {
          localScope[param] = instance;
        }
      }
      this.pushScope(localScope);
      try {
        for (const stmt of initFn.body) {
          this.execute(stmt);
        }
      } catch (e) {
        if (!(e instanceof ReturnSignal)) throw e;
      } finally {
        this.popScope();
      }
    } else if (args.length > 0) {
      throw new RuntimeError(
        `${klass.__pyname__}() takes no arguments (got ${args.length})`
      );
    }
    return instance;
  }

  // === Statement visitors ===

  visit_ExpressionStatement(node: ExpressionStatementNode): unknown {
    return this.execute(node.expression);
  }

  visit_Block(node: BlockNode): unknown {
    for (const stmt of node.statements) {
      this.execute(stmt);
    }
    return null;
  }

  visit_IfStatement(node: IfStatementNode): unknown {
    if (isTruthy(this.execute(node.condition))) {
      for (const stmt of node.body) {
        this.execute(stmt);
      }
    } else if (node.elseBody) {
      for (const stmt of node.elseBody) {
        this.execute(stmt);
      }
    }
    return null;
  }

  visit_WhileStatement(node: WhileStatementNode): unknown {
    while (isTruthy(this.execute(node.condition))) {
      try {
        for (const stmt of node.body) {
          this.execute(stmt);
        }
      } catch (e) {
        if (e instanceof BreakSignal) break;
        if (e instanceof ContinueSignal) continue;
        throw e;
      }
    }
    return null;
  }

  visit_ForStatement(node: ForStatementNode): unknown {
    const iterable = this.execute(node.iterable);
    const items = toArray(iterable);
    for (const item of items) {
      this.currentScope[node.target] = item;
      try {
        for (const stmt of node.body) {
          this.execute(stmt);
        }
      } catch (e) {
        if (e instanceof BreakSignal) break;
        if (e instanceof ContinueSignal) continue;
        throw e;
      }
    }
    return null;
  }

  visit_ReturnStatement(node: ReturnStatementNode): never {
    const value = node.value ? this.execute(node.value) : null;
    throw new ReturnSignal(value);
  }

  visit_BreakStatement(_node: BreakStatementNode): never {
    throw new BreakSignal();
  }

  visit_ContinueStatement(_node: ContinueStatementNode): never {
    throw new ContinueSignal();
  }

  visit_FunctionDefinition(node: FunctionDefinitionNode): unknown {
    const closure: Record<string, unknown> = { ...this.currentScope };
    const fn = makePyFunction(node.name, node.parameters, node.body, closure);
    this.currentScope[node.name] = fn;
    return null;
  }

  visit_ClassDefinition(node: ClassDefinitionNode): unknown {
    // Evaluate the body in a new scope to register any methods/functions
    const klass: any = {
      __pyname__: node.name,
      methods: {},
    };
    this.currentScope[node.name] = klass;
    for (const stmt of node.body) {
      this.execute(stmt);
    }
    return null;
  }

  visit_ImportStatement(node: ImportStatementNode): unknown {
    // Simplified: create a module namespace with no names (or just the module name)
    this.currentScope[node.module] = makeTuple([]);
    return null;
  }

  visit_FromImportStatement(node: FromImportStatementNode): unknown {
    // Simplified: no-op
    return null;
  }
}
