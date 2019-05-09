"""Example Flask app with Flasgger"""

from flask import Flask, Response
from flasgger import Swagger
import logging
import json

app = Flask(__name__)
swagger = Swagger(app)

logger = logging.getLogger()


def api_response(resp_dict, status_code):
    response = Response(json.dumps(resp_dict), status_code)
    response.headers["Content-Type"] = "application/json"
    print(response)
    return response


def lambda_handler(event, context):
    logger.debug("Api started")



@app.route('/colors/<palette>/', methods=["GET"])
def colors(palette):
    """Example endpoint returning a list of colors_api by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors_api (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    logger.debug({"palette": palette})
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    logger.debug({"result": result})
    return api_response(result, 200)


if __name__ == "__main__":
    app.run(debug=True)
