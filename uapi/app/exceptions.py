import falcon
import json


def exception_serializer(req, resp, exception):
    representation = exception.to_json()
    resp.body = representation
    resp.content_type = "application/json"


def generic_error_handler(ex, req, resp, params):
    if isinstance(ex, falcon.HTTPError):
        raise ex
    raise AppException(falcon.HTTP_502, str(ex))


class AppException(falcon.HTTPError):
    def __init__(self, status, message=None):
        super().__init__(status, None, description=message)

    def to_json(self):
        return json.dumps({'status': 'error', 'message': self.description})


class ConfigAlreadyExists(Exception):
    def __init__(self, config_name):
        super().__init__(f"Config with name {config_name} already exists.")


class ConfigNotFound(Exception):
    def __init__(self, config_name):
        super().__init__(f"Config name {config_name} not found")


class ConfigNotModified(Exception):
    def __init__(self, config_name):
        super().__init__(f"Config name {config_name} was not modified")
