import logging
from pymongo import MongoClient
from uapi.conf import conf
from .exceptions import *
import hashlib, uuid


class DB(object):
    """
    DB class for managing Mongo connections,
    the connect=False is set to allow proper
    behavior after fork
    """
    _CONN = None

    @staticmethod
    def get_db_conn():
        if DB._CONN is None:
            logging.info("Initiating DB connection")
            DB._CONN = MongoClient(conf.DB_HOST, conf.DB_PORT, connect=False, serverSelectionTimeoutMS=5000)
        else:
            logging.info("DB connection already initiated, using existing DB connection")
        return DB._CONN


class BaseConfigs(object):
    def __init__(self):
        self.db = DB.get_db_conn()[conf.DB_NAME]

    def ping_db(self):
        return self.db.command('ping')


class Users(BaseConfigs):
    """
    Users class is hold all business
    logic around creation,listing,searching and
    updating of users objects
    """

    def __init__(self):
        super().__init__()

    def create_configs(self, user_obj):
        try:
            # If user is not existing yet in DB
            # the self.list_configs(config_obj['name']) function
            # will rise UserNotFound exception
            self.list_users(user_obj['email'])
            # The ConfigNotFound exception wasn't raised, which is mean
            # the config object with provided name already exists in DB
            # gonna rise ConfigAlreadyExists exception
            logging.error("Unable to create new user object, the user name already exists")
            raise UserAlreadyExists(user_obj['email'])
        except UserNotFound:
            # ALL GOOD - create a new user object
            logging.info("Creating new configs object")
            user_obj['password'] = self._hash_password(user_obj['password'])
            self.db.users.insert_one(user_obj)
            del (user_obj['_id'])
            return user_obj

    def list_users(self, email=None):
        if email is None:
            return list(self.db.users.find({}, {"_id": False}))
        else:
            user = self.db.users.find_one({"email": email}, {"_id": False})
            # If user is None, raise UserNotFound exception
            if user:
                return user
            logging.warning(f"User not found in BD, gonna rise UserNotFound exception")
            raise UserNotFound(email)

    def _hash_password(self, password):
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        return hashed_password
