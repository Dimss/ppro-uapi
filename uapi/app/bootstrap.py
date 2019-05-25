import logging
import requests
from pymongo import MongoClient
from uapi.conf import conf
from .resources import *


def init_routes(api):
    liveness = LivenessResource()
    readiness = ReadinessResource()
    user_resource = UserResource()
    jwt_resource = JWTResource()
    # Liveness and Readiness routes
    api.add_route('/ready', readiness)
    api.add_route('/healthy', liveness)
    # app routes
    api.add_route('/user', user_resource)
    api.add_route('/user/{email}', user_resource)
    api.add_route('/jwt', jwt_resource)
    api.add_route('/jwt/{token}', jwt_resource)


def populate_system_data():
    admin_user = {
        "email": "admin@admin",
        "firstName": "admin",
        "lastName": "admin",
        "password": "admin",
    }

    # The app server running with preload mode,
    # as a result the MongoClient can't be forked
    # open and close connection locally to not cause conn error after fork

    conn = MongoClient(
        conf.DB_HOST,
        conf.DB_PORT,
        username=conf.DB_USER,
        password=conf.DB_PASS,
        connect=False,
        serverSelectionTimeoutMS=5000,
        authSource=conf.DB_NAME
    )
    db = conn[conf.DB_NAME]
    try:
        Users(db).create_user(admin_user, 'admin')
    except UserAlreadyExists:
        logging.warning("The admin user already exists in the DB")
    conn.close()
