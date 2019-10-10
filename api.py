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

# Mock user database
all_users = {
        '1': {"firstName": "Fake Name", "lastName": "surname", "age": 5},
        '2': {"firstName": "Test Name", "lastName": "last name", "age": 1000}
    }


@app.route('/users/<user_id>/', methods=["GET"])
def get_user(user_id):
    if user_id in all_users:
        return api_response(all_users[user_id], 200)
    else:
        return api_response(None, 404)


@app.route('/users/', methods=["GET"])
def get_users():
    response_data = list(all_users.values())
    return api_response(response_data, 200)


@app.route('/users/', methods=["POST"])
def create_user():
    request_data = request.json
    openapi_validate(request_data, 'User', resolved_schema)

    # TODO: save created user and set user_id

    return api_response(request_data, 201)


@app.route('/users/resend-invite/<user_id>/', methods=["PUT"])
def resend_invite_to_user(user_id):
    request_data = request.json
    return api_response(request_data, 200)


if __name__ == "__main__":
    app.run(debug=True)
