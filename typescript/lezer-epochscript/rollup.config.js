import { nodeResolve } from "@rollup/plugin-node-resolve";

export default {
  input: "src/index.js",
  output: {
    file: "dist/index.js",
    format: "es",
    sourcemap: true,
  },
  external: [
    "@lezer/lr",
    "@lezer/highlight",
    "@codemirror/language",
  ],
  plugins: [nodeResolve()],
};
