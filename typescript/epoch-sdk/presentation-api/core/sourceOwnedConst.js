"use strict";
const {getSchemaUtils}=require("./schemas/builders/schema-utils");
exports.sourceOwnedConst=function(schema,expected){
    const check=(direction,value,options)=>value===expected?schema[direction](value,options):
        {ok:false,errors:[{path:options?.breadcrumbsPrefix??[],message:"Value differs from source constant"}]};
    const exact={...schema,parse:(value,options)=>check("parse",value,options),json:(value,options)=>check("json",value,options)};
    return Object.assign(exact,getSchemaUtils(exact));
};
