"""Source-owned outbound validation, without a second model/route schema."""
import json
from functools import lru_cache
from importlib.resources import files
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
URI = "https://epoch.trade/contracts/platform-presentations-v2"
@lru_cache
def validator(name):
    document = json.loads(files("epoch_sdk").joinpath("data/platform-presentations.openapi.json").read_text())
    resource = Resource.from_contents({**document, "$schema":"https://json-schema.org/draft/2020-12/schema"})
    return Draft202012Validator({"$ref":URI+"#/components/schemas/"+name}, registry=Registry().with_resource(URI,resource))
def validate_request(name, value):
    error = next(validator(name).iter_errors(value), None)
    if error is not None:
        raise ValueError("Platform presentation request fails source constraint: " + str(error.validator))
