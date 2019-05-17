import logging
import falcon
from .exceptions import *
from .users import Users, BaseUser
from .jwt import JWTGenerator, JWTValidator
from .validators import create_user_req_schema, update_user_req_schema, create_user_jwt_token_req_schema


class BaseResource(object):

    def __init__(self):
        self.message = None
        self.payload = None
        self.status = falcon.HTTP_200

    def resource_permissions(self):
        return {'public': []}


class UserResource(BaseResource):
    def resource_permissions(self):
        return {'public': ['post']}

    def on_get(self, req, resp, email=None):
        try:
            # Only users with admin role can list users
            if req.context.user['role'] != 'admin':
                self.payload = Users().list_users(req.context.user['sub'])
            else:
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
            self.payload = Users().create_user(user)
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
        try:
            if req.context.user['role'] != 'admin' and email != req.context.user['sub']:
                logging.warning(f"Insufficient resource permissions for user: {req.context.user['sub']}")
                raise AppException(falcon.HTTP_403, "Forbidden")
            Users().update_user(email, user_obj)
        except UserNotFound:
            raise AppException(falcon.HTTP_404, f"User {email} not found")
        except UserNotModified:
            raise AppException(falcon.HTTP_304)

    def on_delete(self, req, resp, email):
        if email is None:
            raise AppException(falcon.HTTP_406, "Missing config name")
        try:
            if req.context.user['role'] != 'admin':
                logging.warning(f"Insufficient resource permissions for user: {req.context.user['sub']}")
                raise AppException(falcon.HTTP_403, "Forbidden")
            Users().delete_user(email)
        except UserNotFound:
            raise AppException(falcon.HTTP_404, f"User {email} not found")


class JWTResource(BaseResource):

    def resource_permissions(self):
        return {'public': ['get', 'post']}

    def on_get(self, req, resp, token):
        try:
            jwt_validator = JWTValidator(token)
            jwt_validator.validate_auth_data()
        except Exception as ex:
            logging.error(f"error during validating token: {str(ex)}")
            raise AppException(falcon.HTTP_401, "Unauthorized")

    @falcon.before(create_user_jwt_token_req_schema)
    def on_post(self, req, resp):
        creds = req.context.get('doc')
        try:
            jwt = JWTGenerator(**creds)
            jwt.authenticate()
            self.payload = jwt.generate_auth_data()
        except WrongPassword:
            raise AppException(falcon.HTTP_401, "Unauthorized")
        except UserNotFound:
            raise AppException(falcon.HTTP_401, "Unauthorized")


class LivenessResource(BaseResource):
    def resource_permissions(self):
        return {'public': ['get']}

    def on_get(self, req, resp):
        pass


class ReadinessResource(BaseResource):
    def resource_permissions(self):
        return {'public': ['get']}

    def on_get(self, req, resp):
        try:
            BaseUser().ping_db()
        except Exception as ex:
            raise AppException(falcon.HTTP_502, "DB is not available yet")
