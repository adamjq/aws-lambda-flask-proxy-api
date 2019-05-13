import json
import os
from werkzeug.exceptions import abort
from jsonschema import validate
import logging
from flask import Response
from prance import ResolvingParser


def get_schema():
    schema_dir = os.path.dirname(os.path.realpath(__file__)) + "/../schema"
    with open(f"{schema_dir}/users-spec.json", 'r') as schema_file:
        return json.load(schema_file)


def resolve_schema_refs(schema) -> dict:
    parser = ResolvingParser(spec_string=schema)
    return parser.specification


def validation_error_inform_error(err, data, schema):
    """
    Custom validation error handler which produces 400 Bad Request
    response in case validation fails and returns the error
    """
    logging.error("API validation error: %s", json.dumps({"error": str(err), "data": data, "schema": schema}))
    abort(Response(json.dumps({"error": str(err), "schema": schema}), status=400))


def api_response(resp_dict, status_code):
    response = Response(json.dumps(resp_dict), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


def openapi_validate(data, component, schema):
    """
    Custom validation function for Flask requests.
    Validates a request body against an component in a openapi3.0 template as Flasgger only validates swagger2.0
    """
    components = schema["components"]["schemas"]
    if component in components:
        try:
            validate(instance=data, schema=components[component])
        except Exception as err:
            validation_error_inform_error(err, data, schema)
