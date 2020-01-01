import uuid
from datetime import datetime
from typing import TypeVar, Type
from flask import session

from .blog import Blog
from ..utils.database import MongoDB
from ..utils.logger import Logger

# declare variables
logger = Logger().logger
T = TypeVar('T', bound='User')


class User:

    COLLECTION = 'users'

    def __init__(self, email: str, password: str, _id: str = None) -> None:
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls: Type[T], email: str) -> T:
        user_info = MongoDB.find_one(collection=cls.COLLECTION,
                                     query={'email': email})
        if user_info is not None:
            return cls(**user_info)

    @classmethod
    def get_by_user_id(cls: Type[T], user_id) -> 'User':  # (factory method)
        user_info = MongoDB.find_one(collection=cls.COLLECTION,
                                     query={'_id': user_id})
        if user_info is not None:
            return cls(**user_info)

    @staticmethod
    def is_login_valid(email: str, password: str) -> bool:
        user_info = User.get_by_email(email=email)
        if user_info is not None:
            return user_info.password == password
        else:
            logger.info('Please register as a new user.')
            return False

    @classmethod
    def register(cls, email: str, password: str):
        if User.get_by_email(email) is not None:
            logger.info('A user with {0} already exist. '
                        'Please login with your registered {0} and password.'
                        .format(email))
        else:
            cls(email, password).save_to_mongo()
            logger.info('Successfully registered new user: {}'.format(email))
            session['email'] = email

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        # is_login_valid has been called
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def create_new_blog(self, title, description):
        Blog(author=self.email,
             author_id=self._id,
             title=title,
             description=description).save_to_mongo()

    @staticmethod
    def create_new_post(blog_id, title, content, date=datetime.utcnow()):
        blog = Blog.get_from_mongo(blog_id)
        blog.create_new_post(title=title, content=content, date=date)

    def json(self) -> dict:
        return dict(email=self.email,
                    password=self.password,
                    _id=self._id)

    def save_to_mongo(self):
        MongoDB.insert(collection=User.COLLECTION, data=self.json())

    @property
    def id(self):
        return self._id
