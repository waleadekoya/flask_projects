__author__ = 'wale'

# import external libraries
import uuid
from flask import session

# import local modules
from database import MongoDB
from logger import Logger

# Initialise variables
log = Logger().logger
dB = MongoDB()


class User:

    REGISTERED_MSG = '{} is already registered. Please sign in.'

    def __init__(self, first_name, last_name, email, password, _user_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self._user_id = uuid.uuid4().hex if _user_id is None else _user_id

    @classmethod
    def get_by_email(cls, email):
        response = dB.find_one(collection='users', query={'email': email})
        if response is not None:
            return cls(**response)

    @classmethod
    def get_by_id(cls, user_id):
        response = dB.find_one(collection='users', query={'_id': user_id})
        if response is not None:
            return cls(**response)

    @staticmethod
    def login_valid(email: str, password: str) -> bool:
        # checks if a user's email matches the password supplied supplied
        # User.login_valid("wale.adekoya@yahoo.com", "123456789")
        user = User.get_by_email(email)
        if user is not None:
            return password == user.password
        return False

    @classmethod
    def register(cls, first_name, last_name, email, password):
        user = cls.get_by_email(email)
        if user is not None:
            # User exist in the Database
            return log.info(cls.REGISTERED_MSG.format(email))
        else:
            # User doesn't exist
            new_user = cls(first_name, last_name, email, password)
            new_user.save_to_db()
            session['email'] = email
            return True

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    @property
    def json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            '_user_id': self._user_id,
            'password': self.password
        }

    def save_to_db(self):
        return dB.insert(collection='users', data=self.json)


class UserDB:

    REGISTERED_MSG = '{} is already registered. Please sign in.'

    def __init__(self, first_name, last_name, email, password, _user_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self._user_id = _user_id

    @property
    def json(self):
        return dict(first_name=self.first_name, last_name=self.last_name,
                    email=self.email, password=self.password,
                    _user_id=self._user_id)

    def register(self):
        try:
            dB.insert(collection='users', data=self.json)
            session['email'] = self.json['email']
        except Exception as e:
            print(e)
            return log.info(UserDB.REGISTERED_MSG.format(self.email))

