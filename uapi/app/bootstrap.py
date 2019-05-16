from .resources import *


def init_routes(api):
    user_resource = UserResource()
    api.add_route('/user', user_resource)
