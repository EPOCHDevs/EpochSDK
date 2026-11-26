"use strict";
const Ajv2020 = require("ajv/dist/2020").default;
const {getSchemaUtils} = require("./schemas/builders/schema-utils");
const {getObjectLikeUtils} = require("./schemas/builders/object-like");
const {getObjectUtils} = require("./schemas/builders/object/object");
const document = require("../../platform-presentations.openapi.json");
const uri = "https://epoch.trade/contracts/platform-presentations-v2";
const ajv = new Ajv2020({allErrors:true,strict:true});
// OpenAPI's named schema container is registry metadata, not a validation
// keyword. Keep the original local pointers; only referenced schemas compile.
ajv.addKeyword({keyword:"components",schemaType:"object",valid:true});
ajv.addSchema({$schema:"https://json-schema.org/draft/2020-12/schema",components:document.components},uri);
exports.platformRequestSchema = function(schema, name) {
    const validate = ajv.compile({$ref:uri+"#/components/schemas/"+name});
    const exact = {...schema,json:(value,options)=>{
        const result=schema.json(value,options);
        if (!result.ok || validate(result.value)) return result;
        return {ok:false,errors:validate.errors.map(error=>({path:[...(options?.breadcrumbsPrefix??[]),...error.instancePath.split("/").filter(Boolean)],message:`Platform request fails ${error.keyword}`}))};
    }};
    return Object.assign(exact,getSchemaUtils(exact),getObjectLikeUtils(exact),getObjectUtils(exact));
};
