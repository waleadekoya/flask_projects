from .post import Post
from ..utils.database import MongoDB

import uuid
from datetime import datetime

mongo_db = MongoDB()


class Blog:
    COLLECTION = 'blogs'

    def __init__(self, *, title, author, description, author_id, _id=None):
        self.title = title
        self.author = author
        self.author_id = author_id
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    @property
    def id(self):
        return self._id

    def create_new_post(self, title, content, date=datetime.utcnow()):
        Post(blog_id=self._id,
             title=title,
             content=content,
             author=self.author,
             created_date=date).save_to_mongo()

    def get_posts(self):
        return Post.get_posts_from_blog_id(blog_id=self._id)

    def json(self):
        return dict(title=self.title,
                    author=self.author,
                    author_id=self.author_id,
                    description=self.description,
                    _id=self._id)

    @classmethod
    def get_from_mongo(cls, blog_id):
        blog_data: dict = mongo_db.find_one(collection=cls.COLLECTION,
                                            query={'_id': blog_id})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs: dict = mongo_db.find(collection=cls.COLLECTION,
                                    query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]

    def save_to_mongo(self):
        mongo_db.insert(collection=Blog.COLLECTION, data=self.json())
