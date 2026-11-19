#!/usr/bin/env node
// Copied from EPOCHDevs/EpochBackend scripts/patch_fern_typescript_record_keys.mjs at 381ca0292d (ENG-2819). The Files
// client runs the same pinned Fern generators, so it needs the same fixes. Change both copies
// together while EpochBackend still generates StratifyX.

// Pinned Fern 0.51.7 reconstructs a record with Object.assign. A legal JSON
// key named __proto__ invokes the accumulator's prototype setter instead of
// becoming an own data property, silently dropping a caller's value.
import fs from "node:fs";
import path from "node:path";

if (!process.argv[2]) throw new Error("Usage: patch_fern_typescript_record_keys.mjs <sdk-root>");
const file = path.join(path.resolve(process.argv[2]), "core/schemas/builders/record/record.js");
const original = fs.readFileSync(file, "utf8");
const unsafe = "Object.assign(Object.assign({}, acc.value), { [transformedKey.value]: transformedValue.value })";
const safe = "Object.fromEntries([...Object.entries(acc.value), [transformedKey.value, transformedValue.value]])";
const count = (text, needle) => text.split(needle).length - 1;
if (count(original, unsafe) === 0 && count(original, safe) === 1) {
    process.stdout.write("Fern record keys already preserve own data properties.\n");
} else {
    if (count(original, unsafe) !== 1 || count(original, safe) !== 0)
        throw new Error(`${file}: pinned Fern record accumulation changed; inspect before patching`);
    fs.writeFileSync(file, original.replace(unsafe, safe));
    process.stdout.write("Preserved own JSON record keys in the Fern TypeScript serializer.\n");
}
