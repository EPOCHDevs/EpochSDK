import { parser } from "./parser.js";
import { LRLanguage, LanguageSupport } from "@codemirror/language";
import { epochscriptHighlighting } from "./highlight.js";

/**
 * EpochScript language definition for CodeMirror 6
 */
export const epochscriptLanguage = LRLanguage.define({
  name: "epochscript",
  parser: parser.configure({
    props: [epochscriptHighlighting],
  }),
  languageData: {
    commentTokens: { line: "#" },
    closeBrackets: { brackets: ["(", "[", "{", "'", '"'] },
  },
});

/**
 * Language support for EpochScript
 * Use this to add EpochScript support to a CodeMirror editor
 *
 * @example
 * import { EditorState } from "@codemirror/state";
 * import { epochscript } from "@epochlab/lezer-epochscript";
 *
 * const state = EditorState.create({
 *   extensions: [epochscript()],
 * });
 */
export function epochscript() {
  return new LanguageSupport(epochscriptLanguage);
}

// Re-export for advanced usage
export { parser } from "./parser.js";
export { epochscriptHighlighting } from "./highlight.js";
