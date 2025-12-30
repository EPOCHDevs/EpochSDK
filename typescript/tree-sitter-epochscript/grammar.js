/**
 * Tree-sitter Grammar for EpochScript
 * ====================================
 *
 * EpochScript is a constrained DSL for financial strategy definition.
 * This grammar ONLY accepts valid EpochScript syntax.
 *
 * Key features:
 * - Timeframe literals: 1D, 4H, 15m (pandas-style, no quotes)
 * - Pipeline operator: src.c | sma(20) transforms to sma(period=20)(src.c)
 * - Single option shorthand: sma(20) -> sma(period=20) when transform has one option
 * - Lag operator: src.c >> 1 (previous values) -> lag(period=1)(src.c)
 * - Lead operator: src.c << 1 (future values) -> lag(period=-1)(src.c)
 * - Built-in schema types as reserved keywords
 * - Dict literals only allowed in schema constructor kwargs (enforced by compiler)
 * - Two-stage call pattern: component(options)(inputs)
 *
 * Built-in Functions (use fn(args) syntax, NOT fn()(args)):
 * ---------------------------------------------------------
 * Unary math functions (single input):
 *   abs, acos, asin, atan, ceil, cos, cosh, exp, floor, ln, log10,
 *   round, sin, sinh, sqrt, tan, tanh, todeg, torad, trunc
 *
 * Binary signal functions (two inputs):
 *   crossover(a, b)  - true when a crosses above b
 *   crossunder(a, b) - true when a crosses below b
 *   crossany(a, b)   - true when a crosses b in any direction
 *
 * Example:
 *   result = abs(price - sma(20)(price))  // Correct
 *   signal = crossover(fast_ma, slow_ma)  // Correct
 *   wrong = abs()(price)                  // ERROR - built-ins don't use ()()
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

const PREC = {
  pipeline: 1,      // Lowest - left associative chaining
  ternary: 2,
  or: 3,
  and: 4,
  not: 5,
  compare: 6,
  lag: 7,           // >> operator (lag)
  lead: 7,          // << operator (lead) - same precedence as lag
  add: 8,
  mul: 9,
  unary: 10,
  power: 11,
  call: 12,
  subscript: 13,
  attribute: 14,
};

// Built-in schema types (reserved keywords)
const BUILTIN_TYPES = [
  'Time',
  'Duration',
  'Session',
  'SessionAnchor',
  'EventMarkerSchema',
  'SqlStatement',
  'TableReportSchema',
  'CardColumnSchema',
];

// Built-in functions (use fn(args) syntax, not fn()(args))
const BUILTIN_FUNCTIONS = [
  // Unary math functions
  'abs', 'acos', 'asin', 'atan', 'ceil', 'cos', 'cosh',
  'exp', 'floor', 'ln', 'log10', 'round', 'sin', 'sinh',
  'sqrt', 'tan', 'tanh', 'todeg', 'torad', 'trunc',
  // Binary signal functions
  'crossover', 'crossunder', 'crossany',
];

module.exports = grammar({
  name: 'epochscript',

  // Whitespace and comments are automatically skipped
  extras: $ => [
    /\s/,
    $.comment,
  ],

  // Word boundary for keywords
  word: $ => $.identifier,

  // No conflicts needed - grammar is unambiguous

  rules: {
    // =========================================================================
    // MODULE (Entry Point)
    // =========================================================================

    module: $ => repeat($._statement),

    // =========================================================================
    // STATEMENTS
    // =========================================================================

    _statement: $ => choice(
      $.assignment_statement,
      $.expression_statement,
    ),

    // Assignment: var = expr
    assignment_statement: $ => seq(
      field('left', $._assignment_target),
      '=',
      field('right', $.expression),
    ),

    _assignment_target: $ => choice(
      $.identifier,
      $.tuple_pattern,
    ),

    // Tuple unpacking: a, b, c
    tuple_pattern: $ => seq(
      $.identifier,
      repeat1(seq(',', $.identifier)),
      optional(','),
    ),

    // Expression as statement
    expression_statement: $ => $.expression,

    // Comments: # text
    comment: $ => token(seq('#', /.*/)),

    // =========================================================================
    // EXPRESSIONS
    // =========================================================================

    expression: $ => choice(
      $.pipeline_expression,
      $.ternary_expression,
      $.or_expression,
      $.and_expression,
      $.not_expression,
      $.comparison_expression,
      $.lag_expression,
      $.lead_expression,
      $.binary_expression,
      $.unary_expression,
      $.power_expression,
      $.call_expression,
      $.attribute_expression,
      $.subscript_expression,
      $.parenthesized_expression,
      $.builtin_type,
      $.builtin_function,
      $.identifier,
      $.timeframe,
      $.integer,
      $.float,
      $.string,
      $.true,
      $.false,
      $.none,
      $.list_literal,
      $.tuple_literal,
      $.dict_literal,
    ),

    // =========================================================================
    // PIPELINE OPERATOR: src.c | sma(period=20)
    // =========================================================================

    pipeline_expression: $ => prec.left(PREC.pipeline, seq(
      field('left', $.expression),
      '|',
      field('right', $.expression),
    )),

    // =========================================================================
    // LAG OPERATOR: src.c >> 1 (get previous values)
    // =========================================================================

    lag_expression: $ => prec.left(PREC.lag, seq(
      field('value', $.expression),
      '>>',
      field('periods', $.expression),
    )),

    // =========================================================================
    // LEAD OPERATOR: src.c << 1 (get future values)
    // =========================================================================

    lead_expression: $ => prec.left(PREC.lead, seq(
      field('value', $.expression),
      '<<',
      field('periods', $.expression),
    )),

    // =========================================================================
    // TERNARY AND BOOLEAN
    // =========================================================================

    // Ternary: value if condition else other
    ternary_expression: $ => prec.right(PREC.ternary, seq(
      field('body', $.expression),
      'if',
      field('condition', $.expression),
      'else',
      field('orelse', $.expression),
    )),

    // Boolean OR
    or_expression: $ => prec.left(PREC.or, seq(
      field('left', $.expression),
      'or',
      field('right', $.expression),
    )),

    // Boolean AND
    and_expression: $ => prec.left(PREC.and, seq(
      field('left', $.expression),
      'and',
      field('right', $.expression),
    )),

    // Boolean NOT
    not_expression: $ => prec(PREC.not, seq(
      'not',
      field('operand', $.expression),
    )),

    // =========================================================================
    // COMPARISON
    // =========================================================================

    comparison_expression: $ => prec.left(PREC.compare, seq(
      field('left', $.expression),
      field('operator', $.comparison_operator),
      field('right', $.expression),
    )),

    comparison_operator: $ => choice(
      '<',
      '>',
      '<=',
      '>=',
      '==',
      '!=',
    ),

    // =========================================================================
    // ARITHMETIC
    // =========================================================================

    // Binary operators (arithmetic)
    binary_expression: $ => choice(
      // Additive
      prec.left(PREC.add, seq(
        field('left', $.expression),
        field('operator', alias(choice('+', '-'), $.additive_operator)),
        field('right', $.expression),
      )),
      // Multiplicative
      prec.left(PREC.mul, seq(
        field('left', $.expression),
        field('operator', alias(choice('*', '/', '%'), $.multiplicative_operator)),
        field('right', $.expression),
      )),
    ),

    // Unary operators
    unary_expression: $ => prec.right(PREC.unary, seq(
      field('operator', choice('-', '+')),
      field('operand', $.expression),
    )),

    // Power operator (**)
    power_expression: $ => prec.right(PREC.power, seq(
      field('base', $.expression),
      '**',
      field('exponent', $.expression),
    )),

    // =========================================================================
    // POSTFIX EXPRESSIONS (Call, Attribute, Subscript)
    // =========================================================================

    // Function call: func(args) or component(options)(inputs)
    call_expression: $ => prec(PREC.call, seq(
      field('function', $.expression),
      field('arguments', $.argument_list),
    )),

    // Attribute access: obj.attr
    attribute_expression: $ => prec.left(PREC.attribute, seq(
      field('object', $.expression),
      '.',
      field('attribute', $.identifier),
    )),

    // Subscript: tuple[index] - for indexing results
    subscript_expression: $ => prec(PREC.subscript, seq(
      field('value', $.expression),
      '[',
      field('index', $.expression),
      ']',
    )),

    // Argument list: (arg1, arg2, key=value)
    argument_list: $ => seq(
      '(',
      optional(seq(
        $._argument,
        repeat(seq(',', $._argument)),
        optional(','),
      )),
      ')',
    ),

    _argument: $ => choice(
      $.expression,
      $.keyword_argument,
    ),

    keyword_argument: $ => seq(
      field('name', $.identifier),
      '=',
      field('value', $.expression),
    ),

    // =========================================================================
    // PRIMARY EXPRESSIONS
    // =========================================================================

    parenthesized_expression: $ => seq(
      '(',
      $.expression,
      ')',
    ),

    // =========================================================================
    // BUILT-IN TYPES (Reserved Keywords)
    // =========================================================================

    builtin_type: $ => choice(
      'Time',
      'Duration',
      'Session',
      'SessionAnchor',
      'EventMarkerSchema',
      'SqlStatement',
      'TableReportSchema',
      'CardColumnSchema',
    ),

    // =========================================================================
    // BUILT-IN FUNCTIONS (use fn(args) syntax, not fn()(args))
    // =========================================================================

    builtin_function: $ => choice(
      // Unary math functions
      'abs', 'acos', 'asin', 'atan', 'ceil', 'cos', 'cosh',
      'exp', 'floor', 'ln', 'log10', 'round', 'sin', 'sinh',
      'sqrt', 'tan', 'tanh', 'todeg', 'torad', 'trunc',
      // Unary data functions
      'ffill',
      // Binary signal functions
      'crossover', 'crossunder', 'crossany',
      // N-ary functions
      'coalesce', 'conditional_select',
    ),

    // =========================================================================
    // LITERALS
    // =========================================================================

    // Timeframe literals (pandas offset style):
    // Basic: 1D, 4H, 15Min, 30s
    // Start/End: 1ME, 1MS, 1QE, 1QS, 1YE, 1YS
    // Weekly with anchor: 1W-SUN, 1W-MON, 1W-FRI
    // Weekly with ordinal: 1W-MON-1st, 1W-MON-2nd, 1W-FRI-Last
    timeframe: $ => token(choice(
      // Minutes with "Min" suffix: 1Min, 5Min, 15Min
      /[1-9][0-9]*Min/,
      // Weekly with day anchor and optional ordinal: 1W-MON, 1W-FRI-Last
      /[1-9][0-9]*W-(SUN|MON|TUE|WED|THU|FRI|SAT)(-(1st|2nd|3rd|4th|Last))?/,
      // Month/Quarter/Year with Start/End: 1ME, 1MS, 1QE, 1QS, 1YE, 1YS
      /[1-9][0-9]*[MQY][SE]/,
      // Basic: 1D, 4H, 1W, 1M, 1Q, 1Y (seconds, hours, days, weeks)
      /[1-9][0-9]*[sHDWMQY]/,
    )),

    // Integer literals
    integer: $ => token(choice(
      /0/,
      /[1-9][0-9]*/,
    )),

    // Float literals
    float: $ => token(choice(
      // Decimal float: 3.14, .5, 3.
      /[0-9]+\.[0-9]*/,
      /[0-9]*\.[0-9]+/,
      // Exponent float: 1e5, 2.5e-3
      /[0-9]+[eE][+-]?[0-9]+/,
      /[0-9]+\.[0-9]*[eE][+-]?[0-9]+/,
      /[0-9]*\.[0-9]+[eE][+-]?[0-9]+/,
    )),

    // String literals
    string: $ => choice(
      seq("'", optional($.string_content_single), "'"),
      seq('"', optional($.string_content_double), '"'),
      seq("'''", optional($.string_content_triple_single), "'''"),
      seq('"""', optional($.string_content_triple_double), '"""'),
    ),

    // String contents (using token.immediate to avoid whitespace issues)
    string_content_single: $ => token.immediate(prec(1, /[^'\\]*(\\.[^'\\]*)*/)),
    string_content_double: $ => token.immediate(prec(1, /[^"\\]*(\\.[^"\\]*)*/)),
    string_content_triple_single: $ => token.immediate(prec(1, /([^']|'[^']|''[^'])*/)),
    string_content_triple_double: $ => token.immediate(prec(1, /([^"]|"[^"]|""[^"])*/)),

    // Boolean literals
    true: $ => 'True',
    false: $ => 'False',

    // None literal
    none: $ => 'None',

    // =========================================================================
    // CONTAINER LITERALS
    // =========================================================================

    // List: [1, 2, 3]
    list_literal: $ => seq(
      '[',
      optional(seq(
        $.expression,
        repeat(seq(',', $.expression)),
        optional(','),
      )),
      ']',
    ),

    // Tuple: (a, b) or (a,) - note: (a) is parenthesized_expression
    tuple_literal: $ => choice(
      // Empty tuple
      seq('(', ')'),
      // Single element tuple (requires trailing comma)
      seq('(', $.expression, ',', ')'),
      // Multi-element tuple
      seq(
        '(',
        $.expression,
        repeat1(seq(',', $.expression)),
        optional(','),
        ')',
      ),
    ),

    // Dict: {key: value, ...} - only allowed in schema constructor kwargs
    // Keys can be identifiers (Success, Error) or strings ("Success")
    dict_literal: $ => seq(
      '{',
      optional(seq(
        $.dict_entry,
        repeat(seq(',', $.dict_entry)),
        optional(','),
      )),
      '}',
    ),

    dict_entry: $ => seq(
      field('key', choice($.identifier, $.string)),
      ':',
      field('value', $.expression),
    ),

    // =========================================================================
    // LEXICAL ELEMENTS
    // =========================================================================

    // Identifier: starts with letter or underscore
    // Cannot be a reserved keyword
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,
  },
});
