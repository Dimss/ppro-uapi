import logging
import falcon
from .users import Users
from .validators import create_user_req_schema


class BaseResource(object):
    def __init__(self):
        self.message = None
        self.payload = None
        self.status = falcon.HTTP_200


class UserResource(BaseResource):
    def on_get(self, req, resp, email=None):
        self.payload = Users().list_users(email)

    @falcon.before(create_user_req_schema)
    def on_post(self, req, resp):
        user = req.context.get('doc')
        self.payload = Users().create_configs(user)
        self.status = falcon.HTTP_201
