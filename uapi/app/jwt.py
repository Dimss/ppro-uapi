import falcon
import logging
from .exceptions import *
from .users import Users
from uapi.conf import conf
import hashlib, binascii, os
import jwt
import time


class JWTGenerator(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.user = self.get_user()
        self._authenticated = False

    def get_user(self):
        try:
            # Make sure user exists
            return Users().list_users(self.email, True)
        except UserNotFound as ex:
            # Raise user not found exception
            raise ex

    def authenticate(self):
        # Validate user's password
        salt = self.user['password'][:64]
        stored_password = self.user['password'][64:]
        hash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt.encode('ascii'), 100000)
        hash = binascii.hexlify(hash).decode('ascii')
        # if hashes are equal, all good, set internal state to authenticated
        if hash == stored_password:
            self._authenticated = True
        else:
            # Raise exception, wrong password
            logging.warning(f"Bad password for user {self.email}")
            raise WrongPassword(self.email)

    def generate_auth_data(self):
        if self._authenticated is False:
            raise WrongPassword(self.email)
        payload = {'sub': self.email, 'iis': 'uapi', "role": self.user['role'], "exp": int(time.time()) + conf.JWT_TTL}
        token = jwt.encode(payload, conf.JWT_SECRET, algorithm=conf.JWT_ALGO).decode('utf-8')
        return {'token': token, 'email': self.email, 'role': self.user['role']}


class JWTValidator(object):
    def __init__(self, token):
        self.token = token

    def validate_auth_data(self):
        try:
            return jwt.decode(self.token, conf.JWT_SECRET, algorithms=conf.JWT_ALGO)
        except Exception as ex:
            logging.error(f"Bad token, {str(ex)}")
            raise BadToken()
