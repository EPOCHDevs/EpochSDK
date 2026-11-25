"use strict";
const Ajv2020 = require("ajv/dist/2020").default;
const {getSchemaUtils} = require("./schemas/builders/schema-utils");
const {getObjectLikeUtils} = require("./schemas/builders/object-like");
const {getObjectUtils} = require("./schemas/builders/object/object");
exports.platformRequestSchema = function(schema, definition) {
    const validate = new Ajv2020({allErrors: true, strict: true}).compile(definition);
    const exact = {...schema, json: (value, options) => {
        const result = schema.json(value, options);
        if (!result.ok || validate(result.value)) return result;
        return {ok: false, errors: validate.errors.map(error => ({
            path: [...(options?.breadcrumbsPrefix ?? []), ...error.instancePath.split("/").filter(Boolean)],
            message: `Platform request fails ${error.keyword}`,
        }))};
    }};
    return Object.assign(exact, getSchemaUtils(exact), getObjectLikeUtils(exact), getObjectUtils(exact));
};
