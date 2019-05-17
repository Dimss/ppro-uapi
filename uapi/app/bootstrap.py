import logging
from .resources import *
from .users import Users


def init_routes(api):
    user_resource = UserResource()
    jwt_resource = JWTResource()

    api.add_route('/user', user_resource)
    api.add_route('/user/{email}', user_resource)
    api.add_route('/jwt', jwt_resource)
    api.add_route('/jwt/{token}', jwt_resource)


def populate_system_data():
    admin_user = {
        "email": "admin@myapp.com",
        "firstName": "admin",
        "lastName": "admin",
        "password": "admin"
    }
    try:
        Users().create_user(admin_user, "admin")
    except UserAlreadyExists:
        logging.warning("The admin user already exists in the DB")
