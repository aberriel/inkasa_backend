from config import current_config
from datetime import date
from hr_2020_app.hr_2020_domain.basic_entity import BasicEntity
from itsdangerous import (
    BadSignature,
    SignatureExpired,
    TimedJSONWebSignatureSerializer as Serializer)
from marshmallow import fields, post_load

import bcrypt
import hashlib


class User(BasicEntity):
    def __init__(self,
                 username: str,
                 password: str = None,
                 name: str = None,
                 birthdate: date = None,
                 _id: str = None):
        super(User, self).__init__(_id=_id)
        self.name = name
        self.username = username
        self.password = password
        self.birthdate = birthdate

    def set_password(self, password: str):
        encoded_password = self._encode_password(password)
        self.password = encoded_password

    @staticmethod
    def _encode_password(password: str):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def _check_password(self, password: str):
        return bcrypt.checkpw(password, self.password)

    def authenticate(self, login: str, password: str):
        return login == self.username and self._check_password(password)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_config.TOKEN_SECRET_KEY, expires_in=expiration)
        return s.dumps({'_id': self._id})

    class Schema(BasicEntity.Schema):
        name = fields.Str(required=False, allow_none=True)
        username = fields.String(required=True, allow_none=False)
        password = fields.String(required=True, allow_none=False)
        birthdate = fields.Date(required=False, allow_none=True, format='iso')

        @post_load
        def post_load(self, data, many, partial):
            return User(**data)
