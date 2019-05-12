"""Example Flask app with Flasgger"""

from flask import Flask, request, Response, jsonify
from flasgger import Swagger, swag_from
import logging
import json
import os
import jsonschema
from werkzeug.exceptions import abort

logger = logging.getLogger()
logger.setLevel('DEBUG')

app = Flask(__name__)


def get_schema():
    schema_dir = os.path.dirname(os.path.realpath(__file__)) + "/../schema"
    with open(f"{schema_dir}/users-spec.json", 'r') as schema_file:
        return json.load(schema_file)


def validation_error_inform_error(err, data, schema):
    """
    Custom validation error handler which produces 400 Bad Request
    response in case validation fails and returns the error
    """
    logging.error("API validation error: %s", json.dumps({"error": str(err), "data": data, "schema": schema}))
    abort(Response(json.dumps({"error": str(err), "schema": schema}), status=400))


def custom_openapi_validate(data, component, schema):
    """
    Custom validation function for Flask requests.
    Validates a request body against an component in a openapi3.0 template as Flasgger only validates swagger2.0
    """
    components = schema.get("components")
    if components is not None:
        schemas = components.get("schemas")
        if schemas is not None and component in schemas:
            try:
                jsonschema.validate(instance=data, schema=schemas[component])
            except jsonschema.exceptions.ValidationError as err:
                validation_error_inform_error(err, data, schema)

swagger = Swagger(
    app,
    template=get_schema()
)


def api_response(resp_dict, status_code):
    response = Response(json.dumps(resp_dict), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/users/<user_id>/', methods=["GET"])
def get_user(user_id):
    """Returns a user if one exists
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: the id of the user
    definitions:
      User:
        type: object
        properties:
          firstName:
            type: string
          lastName:
            type: string
          age:
            type: number
    responses:
      200:
        description: A user
        schema:
          $ref: '#/definitions/User'
        examples:
          '1': {"firstName": "Adam", "lastName": "test", "age": 100}
      404:
         description: No user exists
    """
    all_users = {
        '1': {"firstName": "Adam1", "lastName": "test1", "age": 100},
        '2': {"firstName": "Adam2", "lastName": "test2", "age": 1000}
    }
    if user_id in all_users:
        return api_response(all_users[user_id], 200)
    else:
        return api_response(None, 404)


@app.route('/users/', methods=["POST"])
def create_user():
    """Creates a user
    ---
    parameters:
      - name: user
        in: body
        type: string
        required: true
        description: the user to create
        schema:
          $ref: '#/definitions/User'
    definitions:
      User:
        type: object
        properties:
          firstName:
            type: string
          lastName:
            type: string
          age:
            type: number
    responses:
      201:
        description: User was successfully created
        schema:
          $ref: '#/definitions/User'
        examples:
          '1': {"firstName": "first", "lastName": "last", "age": 100}
    """

    swagger_doc = swagger.template
    custom_openapi_validate(data=request.json, component='User', schema=swagger_doc)

    data = request.json
    return api_response(data, 201)


if __name__ == "__main__":
    app.run(debug=True)
