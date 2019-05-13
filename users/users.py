"""Example Flask app with Flasgger"""

from flask import Flask, request
from flasgger import Swagger
import logging
from api_utils import get_schema, api_response, openapi_validate, resolve_schema_refs


logger = logging.getLogger()
logger.setLevel('DEBUG')

app = Flask(__name__)


schema = get_schema()
resolved_schema = resolve_schema_refs(schema)

swagger = Swagger(
    app,
    template=schema
)


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
        '1': {"firstName": "Adam1", "lastName": "test1", "age": 5},
        '2': {"firstName": "Adam2", "lastName": "test2", "age": 1000}
    }
    if user_id in all_users:
        data = all_users[user_id]
        openapi_validate(data, 'User', resolved_schema)
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
    print(request.json)
    openapi_validate(request.json, 'User', resolved_schema)

    data = request.json
    return api_response(data, 201)


@app.route('/users/', methods=["GET"])
def get_users():
    """Returns a list of all users
    ---
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
        description: A list of all users
        schema:
          $ref: '#/definitions/UsersList'
        examples:
          [{"firstName": "first", "lastName": "last", "age": 100}]
    """

    all_users = [
        {"firstName": "Adam1", "lastName": "test1", "age": 100},
        {"firstName": "Adam2", "lastName": "test2", "age": 1000}
    ]

    data = all_users
    openapi_validate(all_users, 'UsersList', resolved_schema)

    return api_response(data, 200)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
