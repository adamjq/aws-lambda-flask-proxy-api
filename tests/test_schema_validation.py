import unittest
from users.users import custom_openapi_validate
import jsonschema
from werkzeug.exceptions import HTTPException


class SchemaValidation(unittest.TestCase):

    def setUp(self):
        self.valid_single_schema = {
            "openapi": "3.0.0",
            "info": {},
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
            "info": {},
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
        custom_openapi_validate(data=data, component='User', schema=self.valid_single_schema)

    def testOpenApiSingleSchemaInvalidData(self):
        data = {
            "firstName": 100,
            "lastName": "test"
        }
        with self.assertRaises(HTTPException):
            custom_openapi_validate(data=data, component='User', schema=self.valid_single_schema)

    def testOpenApiNestedSchemaValidData(self):
        data = [{
            "age": 20,
            "firstName": "test",
            "lastName": "test"
        }]
        custom_openapi_validate(data=data, component='UsersList', schema=self.valid_nested_schema)


