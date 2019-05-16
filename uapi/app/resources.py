import logging
import falcon


class BaseResource(object):
    def __init__(self):
        self.message = None
        self.payload = None
        self.status = falcon.HTTP_200


class UserResource(BaseResource):
    def on_get(self, req, resp):
        self.payload = {"hello world": "bla"}

    def on_post(self, res, resp):
        pass
