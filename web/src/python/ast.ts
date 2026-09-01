/**
 * TypeScript port of `src/ast/nodes.py`.
 *
 * AST node definitions for the Python-subset interpreter.
 */

import { TokenType } from './lexer';

// === Base classes ===

export interface ASTNode {
  kind: string;
}

export interface Expression extends ASTNode {}
export interface Statement extends ASTNode {}

// === Literals ===

export interface IntegerNode extends Expression {
  kind: 'Integer';
  value: number;
}

export interface FloatNode extends Expression {
  kind: 'Float';
  value: number;
}

export interface StringNode extends Expression {
  kind: 'String';
  value: string;
}

export interface BooleanNode extends Expression {
  kind: 'Boolean';
  value: boolean;
}

export interface NoneLiteralNode extends Expression {
  kind: 'NoneLiteral';
}

export interface VariableNode extends Expression {
  kind: 'Variable';
  name: string;
}

// === Binary / Unary ===

export interface BinaryExpressionNode extends Expression {
  kind: 'BinaryExpression';
  left: Expression;
  operator: TokenType;
  right: Expression;
  operator_value?: string;
}

export interface UnaryExpressionNode extends Expression {
  kind: 'UnaryExpression';
  operator: TokenType;
  operand: Expression;
  operator_value?: string;
}

export interface AssignmentExpressionNode extends Expression {
  kind: 'AssignmentExpression';
  target: Expression;
  value: Expression;
}

export interface FunctionCallNode extends Expression {
  kind: 'FunctionCall';
  func: Expression;
  args: Expression[];
}

export interface SubscriptExpressionNode extends Expression {
  kind: 'SubscriptExpression';
  target: Expression;
  index: Expression;
}

export interface AttributeAccessNode extends Expression {
  kind: 'AttributeAccess';
  target: Expression;
  attribute: string;
}

export interface MethodCallNode extends Expression {
  kind: 'MethodCall';
  target: Expression;
  method: string;
  args: Expression[];
}

export interface ListLiteralNode extends Expression {
  kind: 'ListLiteral';
  elements: Expression[];
}

export interface TupleLiteralNode extends Expression {
  kind: 'TupleLiteral';
  elements: Expression[];
}

export interface DictLiteralNode extends Expression {
  kind: 'DictLiteral';
  entries: Array<[Expression, Expression]>;
}

export interface SetLiteralNode extends Expression {
  kind: 'SetLiteral';
  elements: Expression[];
}

// === Statements ===

export interface ProgramNode extends ASTNode {
  kind: 'Program';
  statements: Statement[];
}

export interface ExpressionStatementNode extends Statement {
  kind: 'ExpressionStatement';
  expression: Expression;
}

export interface FunctionDefinitionNode extends Statement {
  kind: 'FunctionDefinition';
  name: string;
  parameters: string[];
  body: Statement[];
}

export interface IfStatementNode extends Statement {
  kind: 'IfStatement';
  condition: Expression;
  body: Statement[];
  elseBody?: Statement[];
}

export interface ForStatementNode extends Statement {
  kind: 'ForStatement';
  target: string;
  iterable: Expression;
  body: Statement[];
}

export interface WhileStatementNode extends Statement {
  kind: 'WhileStatement';
  condition: Expression;
  body: Statement[];
}

export interface ReturnStatementNode extends Statement {
  kind: 'ReturnStatement';
  value: Expression | null;
}

export interface BreakStatementNode extends Statement {
  kind: 'BreakStatement';
}

export interface ContinueStatementNode extends Statement {
  kind: 'ContinueStatement';
}

export interface ClassDefinitionNode extends Statement {
  kind: 'ClassDefinition';
  name: string;
  body: Statement[];
}

export interface ImportStatementNode extends Statement {
  kind: 'ImportStatement';
  module: string;
}

export interface FromImportStatementNode extends Statement {
  kind: 'FromImportStatement';
  module: string;
  name: string;
}

export interface BlockNode extends Statement {
  kind: 'Block';
  statements: Statement[];
}

export type AnyExpression =
  | IntegerNode | FloatNode | StringNode | BooleanNode | NoneLiteralNode
  | VariableNode | BinaryExpressionNode | UnaryExpressionNode
  | AssignmentExpressionNode | FunctionCallNode | SubscriptExpressionNode
  | AttributeAccessNode | MethodCallNode | ListLiteralNode | TupleLiteralNode
  | DictLiteralNode | SetLiteralNode;

export type AnyStatement =
  | ExpressionStatementNode | FunctionDefinitionNode | IfStatementNode
  | ForStatementNode | WhileStatementNode | ReturnStatementNode
  | BreakStatementNode | ContinueStatementNode | ClassDefinitionNode
  | ImportStatementNode | FromImportStatementNode | BlockNode;

// === Convenience constructors ===

export const Integer = (value: number): IntegerNode => ({ kind: 'Integer', value });
export const Float = (value: number): FloatNode => ({ kind: 'Float', value });
export const Str = (value: string): StringNode => ({ kind: 'String', value });
export const Bool = (value: boolean): BooleanNode => ({ kind: 'Boolean', value });
export const NoneLit = (): NoneLiteralNode => ({ kind: 'NoneLiteral' });
export const Variable = (name: string): VariableNode => ({ kind: 'Variable', name });

export const BinaryExpression = (
  left: Expression,
  operator: TokenType,
  right: Expression,
  operator_value?: string
): BinaryExpressionNode => ({ kind: 'BinaryExpression', left, operator, right, operator_value });

export const UnaryExpression = (
  operator: TokenType,
  operand: Expression,
  operator_value?: string
): UnaryExpressionNode => ({ kind: 'UnaryExpression', operator, operand, operator_value });

export const AssignmentExpression = (
  target: Expression,
  value: Expression
): AssignmentExpressionNode => ({ kind: 'AssignmentExpression', target, value });

export const FunctionCall = (func: Expression, args: Expression[]): FunctionCallNode => ({ kind: 'FunctionCall', func, args });

export const SubscriptExpression = (
  target: Expression,
  index: Expression
): SubscriptExpressionNode => ({ kind: 'SubscriptExpression', target, index });

export const AttributeAccess = (
  target: Expression,
  attribute: string
): AttributeAccessNode => ({ kind: 'AttributeAccess', target, attribute });

export const MethodCall = (target: Expression, method: string, args: Expression[]): MethodCallNode => ({ kind: 'MethodCall', target, method, args });

export const ListLiteral = (elements: Expression[]): ListLiteralNode => ({ kind: 'ListLiteral', elements });
export const TupleLiteral = (elements: Expression[]): TupleLiteralNode => ({ kind: 'TupleLiteral', elements });
export const DictLiteral = (entries: Array<[Expression, Expression]>): DictLiteralNode => ({ kind: 'DictLiteral', entries });
export const SetLiteral = (elements: Expression[]): SetLiteralNode => ({ kind: 'SetLiteral', elements });

export const ExpressionStatement = (expression: Expression): ExpressionStatementNode => ({ kind: 'ExpressionStatement', expression });
export const FunctionDefinition = (
  name: string,
  parameters: string[],
  body: Statement[]
): FunctionDefinitionNode => ({ kind: 'FunctionDefinition', name, parameters, body });

export const IfStatement = (
  condition: Expression,
  body: Statement[],
  elseBody?: Statement[]
): IfStatementNode => ({ kind: 'IfStatement', condition, body, elseBody });

export const ForStatement = (
  target: string,
  iterable: Expression,
  body: Statement[]
): ForStatementNode => ({ kind: 'ForStatement', target, iterable, body });

export const WhileStatement = (
  condition: Expression,
  body: Statement[]
): WhileStatementNode => ({ kind: 'WhileStatement', condition, body });

export const ReturnStatement = (value: Expression | null): ReturnStatementNode => ({ kind: 'ReturnStatement', value });
export const BreakStatement = (): BreakStatementNode => ({ kind: 'BreakStatement' });
export const ContinueStatement = (): ContinueStatementNode => ({ kind: 'ContinueStatement' });

export const ClassDefinition = (name: string, body: Statement[]): ClassDefinitionNode => ({ kind: 'ClassDefinition', name, body });
export const ImportStatement = (module: string): ImportStatementNode => ({ kind: 'ImportStatement', module });
export const FromImportStatement = (module: string, name: string): FromImportStatementNode => ({ kind: 'FromImportStatement', module, name });
export const Block = (statements: Statement[]): BlockNode => ({ kind: 'Block', statements });

export const Program = (statements: Statement[]): ProgramNode => ({ kind: 'Program', statements });