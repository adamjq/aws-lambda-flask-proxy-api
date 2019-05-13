import unittest
from copy import deepcopy
from users.api_utils import openapi_validate, resolve_schema_refs
from werkzeug.exceptions import HTTPException


class SchemaValidation(unittest.TestCase):

    def setUp(self):
        self.valid_schema = {
            "openapi": "3.0.0",
            "info": {
                "description": "powered by Flasgger",
                "termsOfService": "/tos",
                "title": "A swagger API",
                "version": "0.0.1"
            },
            "paths": {},
            "components": {
                "schemas": {
                    "UsersList": {
                        "type": "array",
                        "items": {
                            "$ref": '#/components/schemas/User'
                        }
                    },
                    "User": {
                        "required": ["firstName"],
                        "properties": {
                            "age": {
                                "type": "number"
                            },
                            "firstName": {
                                "type": "string"
                            },
                            "lastName": {
                                "type": "string"
                            }
                        },
                        "type": "object"
                    }
                }
            }
        }

    def testOpenApiSchemaValidData(self):
        data = {
            "age": 50,
            "firstName": "test",
            "lastName": "test"
        }
        schema = resolve_schema_refs(deepcopy(self.valid_schema))
        openapi_validate(data=data, component='User', schema=schema)

    def testOpenApiSchemaValidDataMinimumProperties(self):
        data = {
            "firstName": "test"
        }
        schema = resolve_schema_refs(deepcopy(self.valid_schema))
        openapi_validate(data=data, component='User', schema=schema)

    def testOpenApiSchemaMissingRequiredProperties(self):
        data = {
            "age": 50,
            "lastName": "test"
        }
        schema = resolve_schema_refs(deepcopy(self.valid_schema))
        with self.assertRaises(HTTPException):
            openapi_validate(data=data, component='User', schema=schema)

    def testOpenApiSchemaInvalidData(self):
        data = {
            "age": 50,
            "firstName": 100,
            "lastName": "test"
        }
        schema = resolve_schema_refs(deepcopy(self.valid_schema))
        with self.assertRaises(HTTPException):
            openapi_validate(data=data, component='User', schema=schema)

    def testOpenApiNestedSchemaValidData(self):
        data = [{
            "age": 50,
            "firstName": "test",
            "lastName": "test"
        }]
        schema = resolve_schema_refs(deepcopy(self.valid_schema))
        openapi_validate(data=data, component='UsersList', schema=schema)

    def testOpenApiNestedSchemaInvalidData(self):
        data = [{
            "age": 50,
            "firstName": 100,
            "lastName": "test"
        }]
        schema = resolve_schema_refs(deepcopy(self.valid_schema))
        with self.assertRaises(HTTPException):
            openapi_validate(data=data, component='UsersList', schema=schema)


if __name__ == "__main__":
    unittest.main()


