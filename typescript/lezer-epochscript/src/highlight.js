import { styleTags, tags as t } from "@lezer/highlight";

/**
 * Syntax highlighting tags for EpochScript
 * Maps grammar nodes to CodeMirror highlight tags
 *
 * Note: Literal operators like /, *, (, ), etc. cannot be used as keys
 * because they have special meaning in styleTags path syntax.
 * These operators will use default styling.
 */
export const epochscriptHighlighting = styleTags({
  // Identifiers - use path syntax for context-specific highlighting
  Identifier: t.variableName,
  "CallExpression/AttributeExpression/Identifier": t.function(t.variableName),
  "CallExpression/Identifier": t.function(t.variableName),
  "KeywordArgument/Identifier": t.propertyName,
  "AttributeExpression/Identifier": t.propertyName,

  // Built-in types (Time, Duration, Session, etc.)
  BuiltinType: t.typeName,

  // Built-in functions (abs, sqrt, crossover, etc.) - highlighted as standard library
  BuiltinFunction: t.standard(t.function(t.variableName)),

  // Literals
  Number: t.number,
  String: t.string,
  Boolean: t.bool,
  None: t.null,
  Timeframe: t.special(t.literal),

  // Keywords (space-separated list of keyword names)
  "if else and or not": t.keyword,
  "True False None": t.literal,

  // Named operator nodes from grammar
  ComparisonOp: t.compareOperator,

  // Comments
  Comment: t.lineComment,

  // Container literals
  ListLiteral: t.list,
  TupleLiteral: t.list,
  DictLiteral: t.list,
  DictPair: t.definition(t.propertyName),
});
