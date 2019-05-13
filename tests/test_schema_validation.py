import unittest
from users.api_utils import openapi_validate, resolve_schema_refs
from werkzeug.exceptions import HTTPException


class SchemaValidation(unittest.TestCase):

    def setUp(self):
        self.valid_single_schema = {
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
                    "User": {
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

        self.valid_nested_schema = {
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

    def testOpenApiSingleSchemaValidData(self):
        data = {
            "age": 20,
            "firstName": "test",
            "lastName": "test"
        }
        schema = resolve_schema_refs(self.valid_single_schema)
        openapi_validate(data=data, component='User', schema=schema)

    def testOpenApiSingleSchemaInvalidData(self):
        data = {
            "firstName": 100,
            "lastName": "test"
        }
        schema = resolve_schema_refs(self.valid_single_schema)
        with self.assertRaises(HTTPException):
            openapi_validate(data=data, component='User', schema=schema)

    def testOpenApiNestedSchemaValidData(self):
        data = [{
            "age": 20,
            "firstName": "test",
            "lastName": "test"
        }]
        schema = resolve_schema_refs(self.valid_nested_schema)
        openapi_validate(data=data, component='UsersList', schema=schema)


