import logging
import falcon
from jsonschema import validate
from .exceptions import AppException


def create_user_req_schema(req, resp, resource, params):
    schema = {
        "id": "create_user",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "email",
            "firstName",
            "lastName",
            "password",
        ],
        "properties": {
            "email": {
                "type": "string"
            },
            "firstName": {
                "type": "string",
            },
            "lastName": {
                "type": "string",
            },
            "password": {
                "type": "string",
            }
        }
    }
    try:
        # Validate request payload against json schema
        validate(req.context['doc'], schema)
    except Exception as ex:
        logging.error(f"Error during validating request payload, ex: {ex}")
        raise AppException(falcon.HTTP_406, str(ex))


def update_user_req_schema(req, resp, resource, params):
    schema = {
        "id": "update_user",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "firstName",
            "lastName",
        ],
        "properties": {
            "firstName": {
                "type": "string",
            },
            "lastName": {
                "type": "string",
            }
        }
    }
    try:
        # Validate request payload against json schema
        validate(req.context['doc'], schema)
    except Exception as ex:
        logging.error(f"Error during validating request payload, ex: {ex}")
        raise AppException(falcon.HTTP_406, str(ex))


def create_user_jwt_token_req_schema(req, resp, resource, params):
    schema = {
        "id": "update_user",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "email",
            "password",
        ],
        "properties": {
            "email": {
                "type": "string",
            },
            "password": {
                "type": "string",
            }
        }
    }
    try:
        # Validate request payload against json schema
        validate(req.context['doc'], schema)
    except Exception as ex:
        logging.error(f"Error during validating request payload, ex: {ex}")
        raise AppException(falcon.HTTP_406, str(ex))
