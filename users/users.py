"""Example Flask app with Flasgger"""

from flask import Flask, request, Response, jsonify
from flasgger import Swagger, validate
import logging
import json

logger = logging.getLogger()
logger.setLevel('DEBUG')

app = Flask(__name__)
swagger = Swagger(app)


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
    data = json.loads(request.data)
    print("Creating a user")
    print(data)
    return api_response(data, 201)


if __name__ == "__main__":
    app.run(debug=True)
