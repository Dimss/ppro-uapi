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


class UserAlreadyExists(Exception):
    def __init__(self, email):
        super().__init__(f"User with email {email} already exists.")


class UserNotFound(Exception):
    def __init__(self, email):
        super().__init__(f"User {email} not found")


class UserNotModified(Exception):
    def __init__(self, user):
        super().__init__(f"User {user} was not modified")
