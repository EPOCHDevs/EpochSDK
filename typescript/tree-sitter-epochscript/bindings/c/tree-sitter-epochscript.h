#ifndef TREE_SITTER_EPOCHSCRIPT_H_
#define TREE_SITTER_EPOCHSCRIPT_H_

typedef struct TSLanguage TSLanguage;

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Returns the tree-sitter language for EpochScript.
 *
 * EpochScript is a constrained Python-like DSL for financial strategy definition.
 * This grammar ONLY accepts valid EpochScript syntax - unsupported Python
 * constructs will result in parse errors.
 *
 * Usage:
 *   TSParser *parser = ts_parser_new();
 *   ts_parser_set_language(parser, tree_sitter_epochscript());
 *
 *   const char *source = "x = sma(period=20)(src.c)";
 *   TSTree *tree = ts_parser_parse_string(parser, NULL, source, strlen(source));
 */
const TSLanguage *tree_sitter_epochscript(void);

#ifdef __cplusplus
}
#endif

#endif  // TREE_SITTER_EPOCHSCRIPT_H_
