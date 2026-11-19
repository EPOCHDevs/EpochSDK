#!/usr/bin/env node
// Copied from EPOCHDevs/EpochBackend scripts/patch_fern_typescript_error_bodies.mjs at 381ca0292d (ENG-2819). The Files
// client runs the same pinned Fern generators, so it needs the same fixes. Change both copies
// together while EpochBackend still generates StratifyX.

// Fern 0.51.7 applies binary/stream response decoding to unsuccessful HTTP
// responses too. Typed JSON errors must be decoded before endpoint dispatch,
// while successful content must remain an opaque stream/blob/buffer.
import fs from "node:fs";
import path from "node:path";

if (!process.argv[2]) throw new Error("Usage: patch_fern_typescript_error_bodies.mjs <sdk-root>");
const file = path.join(path.resolve(process.argv[2]), "core/fetcher/Fetcher.js");
let source = fs.readFileSync(file, "utf8");
const originalDecode = "const responseBody = yield (0, getResponseBody_1.getResponseBody)(response, args.responseType);";
const repairedDecode = "const responseBody = yield (0, getResponseBody_1.getResponseBody)(response, response.status >= 200 && response.status < 400 ? args.responseType : undefined);";
const originalError = `            else {
                return {
                    ok: false,
                    error: {
                        reason: "status-code",`;
const repairedError = `            else {
                // Preserve non-JSON and empty error responses, including status.
                if (responseBody === undefined || (responseBody != null && responseBody.ok === false &&
                    responseBody.error != null && responseBody.error.reason === "non-json")) {
                    return {
                        ok: false,
                        error: {
                            reason: "non-json",
                            statusCode: response.status,
                            rawBody: responseBody === undefined ? "" : responseBody.error.rawBody,
                        },
                        rawResponse: (0, RawResponse_1.toRawResponse)(response),
                    };
                }
                return {
                    ok: false,
                    error: {
                        reason: "status-code",`;
const count = (text, needle) => text.split(needle).length - 1;
const original = count(source, originalDecode) === 1 && count(source, originalError) === 1 &&
    count(source, repairedDecode) === 0 && count(source, repairedError) === 0;
const repaired = count(source, originalDecode) === 0 && count(source, originalError) === 0 &&
    count(source, repairedDecode) === 1 && count(source, repairedError) === 1;
if (repaired) {
    process.stdout.write("Fern HTTP error bodies already retain JSON decoding and status.\n");
} else {
    if (!original) throw new Error(`${file}: pinned Fern response handling changed; inspect before patching`);
    source = source.replace(originalDecode, repairedDecode).replace(originalError, repairedError);
    fs.writeFileSync(file, source);
    process.stdout.write("Preserved JSON/non-JSON HTTP errors without decoding successful binary content.\n");
}
