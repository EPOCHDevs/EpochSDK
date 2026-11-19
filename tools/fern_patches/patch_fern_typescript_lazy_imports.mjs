#!/usr/bin/env node
// Copied from EPOCHDevs/EpochBackend scripts/patch_fern_typescript_lazy_imports.mjs at 381ca0292d (ENG-2819). The Files
// client runs the same pinned Fern generators, so it needs the same fixes. Change both copies
// together while EpochBackend still generates StratifyX.

// Fern 0.51.7 implements recursive schema references by eagerly importing the
// complete serialization barrel, even though the reference itself is wrapped
// in lazyObject() or the union serializer's lazy(). A leaf-first require can then re-enter an unfinished model
// (recursive model -> shared barrel -> parent model -> recursive model).
// Keep Fern's generated serializer and defer only that barrel lookup until the
// lazy schema is actually parsed or serialized.

import fs from "node:fs";
import path from "node:path";

const root = process.argv[2];
if (root == null) {
    throw new Error("usage: patch_fern_typescript_lazy_imports.mjs <sdk-root>");
}

const serializationRoot = path.join(path.resolve(root), "serialization");
if (!fs.existsSync(serializationRoot)) {
    // A future Fern layout may not have runtime serializers. Verification owns
    // the required public entry points; there is nothing to rewrite here.
    process.exit(0);
}

const serializerImport =
    /^const serializers = __importStar\(require\(("[^"\r\n]+")\)\);\r?$/m;
const lazySerializerReference =
    /core\.serialization\.(lazyObject|lazy)\(\(\) => serializers\.([A-Za-z_$][\w$]*)\)/g;

const javascriptFiles = [];
const visit = (directory) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
        const target = path.join(directory, entry.name);
        if (entry.isDirectory()) visit(target);
        else if (entry.isFile() && entry.name.endsWith(".js"))
            javascriptFiles.push(target);
    }
};
visit(serializationRoot);

let rewrittenFiles = 0;
let rewrittenReferences = 0;
for (const filename of javascriptFiles) {
    const original = fs.readFileSync(filename, "utf8");
    const importMatch = original.match(serializerImport);
    if (importMatch == null) continue;

    const importPath = importMatch[1];
    let references = 0;
    let rewritten = original.replace(
        lazySerializerReference,
        (_match, wrapper, exportName) => {
            references += 1;
            return `core.serialization.${wrapper}(() => require(${importPath}).${exportName})`;
        },
    );
    if (references === 0) {
        throw new Error(
            `${filename}: eager serializers barrel import is not confined to a supported lazy wrapper`,
        );
    }
    rewritten = rewritten.replace(serializerImport, "");
    if (/\bserializers\b/.test(rewritten)) {
        throw new Error(
            `${filename}: unsupported serializers barrel reference remains after rewrite`,
        );
    }
    fs.writeFileSync(filename, rewritten);
    rewrittenFiles += 1;
    rewrittenReferences += references;
}

process.stdout.write(
    `Deferred ${rewrittenReferences} Fern lazy serializer reference(s) in ` +
        `${rewrittenFiles} file(s).\n`,
);
