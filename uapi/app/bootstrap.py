from .resources import *


def init_routes(api):
    user_resource = UserResource()
    jwt_resource = JWTResource()

    api.add_route('/user', user_resource)
    api.add_route('/user/{email}', user_resource)
    api.add_route('/jwt', jwt_resource)
    api.add_route('/jwt/{token}', jwt_resource)
