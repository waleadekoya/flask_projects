from ..utils.database import MongoDB

import uuid
from datetime import datetime

mongo_db = MongoDB()


class Post:
    COLLECTION = 'posts'

    def __init__(self, *, title, content, author, blog_id,
                 created_date=datetime.utcnow(), _id=None):
        self.title = title
        self.content = content
        self.author = author
        self.blog_id = blog_id
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id  # overwrites default _id in MongoDB

    @property
    def id(self):
        return self._id

    def json(self):
        return dict(title=self.title, content=self.content,
                    author=self.author, blog_id=self.blog_id,
                    created_date=self.created_date, _id=self._id)

    @classmethod
    def get_from_mongo(cls, post_id):
        post_data = mongo_db.find_one(collection=cls.COLLECTION,
                                      query={'_id': post_id})
        return cls(**post_data)

    def save_to_mongo(self):
        mongo_db.insert(collection=Post.COLLECTION,
                        data=self.json())

    @staticmethod
    def get_posts_from_blog_id(blog_id):
        posts_cursor_object = mongo_db.find(collection=Post.COLLECTION,
                                            query={'blog_id': blog_id})
        return [post for post in posts_cursor_object]
