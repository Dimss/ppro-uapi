import logging
from pymongo import MongoClient
from uapi.conf import conf
from .exceptions import *
import hashlib, binascii, os


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

    def create_user(self, user_obj, role='user'):
        try:
            # If user is not existing yet in DB
            # the self.list_configs(config_obj['name']) function
            # will rise UserNotFound exception
            self.list_users(user_obj['email'])
            # The UserNotFound exception wasn't raised, which is mean
            # the user object with provided email already exists in DB
            # gonna rise UserAlreadyExists exception
            logging.error("Unable to create new user object, the user name already exists")
            raise UserAlreadyExists(user_obj['email'])
        except UserNotFound:
            # ALL GOOD - create a new user object
            logging.info("Creating new configs object")
            user_obj['password'] = self.hash_password(user_obj['password'])
            # Append role to user
            user_obj['role'] = role
            # Insert user object ot DB
            self.db.users.insert_one(user_obj)
            # Remove Mongo UUID
            del (user_obj['_id'])
            # Remove password hash
            del (user_obj['password'])
            return user_obj

    def list_users(self, email=None, include_password_hash=False):
        if email is None:
            return list(self.db.users.find({}, {"_id": False, "password": False}))
        else:
            if include_password_hash:
                user = self.db.users.find_one({"email": email}, {"_id": False})
            else:
                user = self.db.users.find_one({"email": email}, {"_id": False, "password": False})
            # If user is None, raise UserNotFound exception
            if user:
                return user
            logging.warning(f"User not found in BD, gonna rise UserNotFound exception")
            raise UserNotFound(email)

    def update_user(self, email, user_obj):
        logging.info(f"Gonna update user {email}")
        # Updating the user document
        update_doc = {
            'firstName': user_obj['firstName'],
            'lastName': user_obj['lastName'],
        }
        res = self.db.users.update_one({'email': email}, {"$set": update_doc})
        if res.matched_count == 0:
            logging.warning(f"User {email} not found ")
            raise UserNotFound(email)
        if res.modified_count == 0:
            logging.warning(f"User {email} not modified")
            raise UserNotModified(email)

    def delete_user(self, email):
        logging.info(f"Gonna delete user {email}")
        # Deleting the config document
        res = self.db.users.delete_one({'email': email})
        if res.deleted_count == 0:
            logging.warning(f"User {email} not found!")
            raise UserNotFound(email)

    def hash_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        hash = binascii.hexlify(hash)
        return (salt + hash).decode('ascii')
        # salt = uuid.uuid4().hex
        # hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        # return hashed_password
