/**
 * Basic tests for EpochScript Lezer grammar
 */

import { parser } from "../dist/parser.js";

const testCases = [
  // Assignments
  { input: "x = 42", shouldParse: true },
  { input: "result = a + b", shouldParse: true },
  { input: "a, b = values", shouldParse: true },

  // Two-stage calls
  { input: "x = sma(period=20)(src.c)", shouldParse: true },
  { input: "src = market_data_source(timeframe=\"1D\")()", shouldParse: true },
  { input: "result = agg_max()(a, b, c)", shouldParse: true },

  // Pipeline operator
  { input: "result = src.c | sma(20)", shouldParse: true },
  { input: "smoothed = price | sma(10) | ema(5)", shouldParse: true },
  { input: "x = data | filter(cond=True) | transform()", shouldParse: true },

  // Lag operator (>>)
  { input: "prev = src.c >> 1", shouldParse: true },
  { input: "prev5 = close >> 5", shouldParse: true },
  { input: "lagged = (high + low) >> 2", shouldParse: true },

  // Lead operator (<<)
  { input: "next = src.c << 1", shouldParse: true },
  { input: "future = close << 3", shouldParse: true },

  // Timeframe literals
  { input: "tf = 1D", shouldParse: true },
  { input: "tf = 4H", shouldParse: true },
  { input: "tf = 15Min", shouldParse: true },
  { input: "tf = 1W", shouldParse: true },
  { input: "tf = 1ME", shouldParse: true },
  { input: "tf = 1QS", shouldParse: true },
  { input: "tf = 1W-MON", shouldParse: true },
  { input: "tf = 1W-FRI-Last", shouldParse: true },
  { input: "src = market_data_source(timeframe=1D)()", shouldParse: true },

  // Built-in types
  { input: "t = Time(hour=9, minute=30)", shouldParse: true },
  { input: "d = Duration(hours=1)", shouldParse: true },
  { input: "s = Session(start=t1, end=t2)", shouldParse: true },
  { input: "anchor = SessionAnchor(session=s)", shouldParse: true },
  { input: "schema = EventMarkerSchema(name=\"test\")", shouldParse: true },

  // Operators
  { input: "x = 1 + 2 * 3 ** 4", shouldParse: true },
  { input: "cond = a > 0 and b < 10", shouldParse: true },
  { input: "output = 1 if cond else 0", shouldParse: true },
  { input: "neg = not flag", shouldParse: true },
  { input: "combo = a or b and c", shouldParse: true },

  // Comparisons
  { input: "cmp = a < b", shouldParse: true },
  { input: "cmp = a <= b", shouldParse: true },
  { input: "cmp = a > b", shouldParse: true },
  { input: "cmp = a >= b", shouldParse: true },
  { input: "cmp = a == b", shouldParse: true },
  { input: "cmp = a != b", shouldParse: true },

  // Literals
  { input: "x = [1, 2, 3]", shouldParse: true },
  { input: "x = (a, b)", shouldParse: true },
  { input: 'x = {"key": "value"}', shouldParse: true },
  { input: 'x = {Success: 1, Error: -1}', shouldParse: true },  // Dict with identifier keys
  { input: "x = True", shouldParse: true },
  { input: "x = False", shouldParse: true },
  { input: "x = None", shouldParse: true },
  { input: "x = 3.14", shouldParse: true },
  { input: "x = 1e-5", shouldParse: true },
  { input: "x = ()", shouldParse: true },  // Empty tuple
  { input: "x = (a,)", shouldParse: true },  // Single element tuple

  // Strings
  { input: 'x = "hello"', shouldParse: true },
  { input: "x = 'world'", shouldParse: true },
  { input: 'x = """multi\nline"""', shouldParse: true },

  // Comments
  { input: "# comment\nx = 1", shouldParse: true },
  { input: "x = 1  # inline", shouldParse: true },

  // Complex expressions
  { input: "signal = 1.0 if close > sma(20)(close) else -1.0", shouldParse: true },
  { input: "spread = (high - low) / close * 100", shouldParse: true },
  { input: "result = func(a, b, opt=True)(x, y)", shouldParse: true },
];

let passed = 0;
let failed = 0;

for (const { input, shouldParse } of testCases) {
  try {
    const tree = parser.parse(input);
    const hasError = tree.toString().includes("⚠");

    if (shouldParse && !hasError) {
      passed++;
      console.log(`✓ ${input.replace(/\n/g, "\\n")}`);
    } else if (!shouldParse && hasError) {
      passed++;
      console.log(`✓ (expected error) ${input.replace(/\n/g, "\\n")}`);
    } else {
      failed++;
      console.log(`✗ ${input.replace(/\n/g, "\\n")}`);
      console.log(`  Expected ${shouldParse ? "success" : "error"}, got ${hasError ? "error" : "success"}`);
      console.log(`  Tree: ${tree.toString()}`);
    }
  } catch (e) {
    failed++;
    console.log(`✗ ${input.replace(/\n/g, "\\n")}`);
    console.log(`  Error: ${e.message}`);
  }
}

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
