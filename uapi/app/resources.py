import logging
import falcon
from .exceptions import *
from .users import Users
from .validators import create_user_req_schema, update_user_req_schema


class BaseResource(object):
    def __init__(self):
        self.message = None
        self.payload = None
        self.status = falcon.HTTP_200


class UserResource(BaseResource):
    def on_get(self, req, resp, email=None):
        try:
            self.payload = Users().list_users(email)
        except UserNotFound:
            raise AppException(falcon.HTTP_404, f"User {email} not found")
        except Exception as ex:
            logging.error(f"Fatal error during fetching user object, ex: {str(ex)}")
            raise AppException(falcon.HTTP_502, "Fatal error during fetching user object")

    @falcon.before(create_user_req_schema)
    def on_post(self, req, resp):
        try:
            user = req.context.get('doc')
            self.payload = Users().create_configs(user)
            self.status = falcon.HTTP_201
        except UserAlreadyExists:
            logging.warning(f"User with provided email {user['email']} already exists")
            raise AppException(falcon.HTTP_409, "User with provided email already exists")
        except Exception as ex:
            logging.error(f"Fatal error during creating user objects, ex: {str(ex)}")
            raise AppException(falcon.HTTP_502, "Fatal error during creating user objects")

    @falcon.before(update_user_req_schema)
    def on_put(self, req, resp, email):
        user_obj = req.context.get('doc')
        Users().update_user(email, user_obj)

    def on_delete(self, req, resp, email):
        if email is None:
            raise AppException(falcon.HTTP_406, "Missing config name")
        try:
            Users().delete_user(email)
        except UserNotFound:
            raise AppException(falcon.HTTP_404, f"User {email} not found")
