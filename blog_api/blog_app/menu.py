from blog import Blog
from utils.database import MongoDB
from utils.logger import Logger

log = Logger().logger


class Menu:

    def __init__(self):
        self.user = input('Enter your author name: ')
        self.user_blog = None
        if self._user_has_account():
            log.info('Welcome back {}'.format(self.user))
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        blog = MongoDB.find_one(collection='blogs', query={'author': self.user})
        if blog is not None:
            # i.e if the blog exist, set the user_blog to the blog
            self.user_blog = Blog.get_from_mongo(blog_id=blog['_id'])
            return True
        return False

    def _prompt_user_for_account(self):
        title = input('Enter blog title: ')
        description = input('Enter blog description: ')
        blog = Blog(title=title,
                    author=self.user,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        read_or_write = input('Will you like to read(R) or write(W): ')
        if read_or_write == 'R':
            # list blogs in database
            self._list_blogs()
            self._view_blogs()
            # allow user to pick one
            # display posts
            pass
        elif read_or_write == 'W':
            # prompt to create a new blog
            self.user_blog.create_new_post()
            pass
        else:
            log.info('Thanks for blogging today!')

    @staticmethod
    def _list_blogs():
        blogs = MongoDB.find(collection='blogs', query={})
        for blog in blogs:
            author = blog['author']
            blog_id = blog['_id']
            title = blog['title']
            log.info('ID: {0}, Title: {0}, Author: {0}'
                     .format(blog_id, title, author))

    @staticmethod
    def _view_blogs():
        blog_id = input('Please enter the blog_id you want to view: ')
        blog = Blog.get_from_mongo(blog_id=blog_id)
        posts = blog.get_posts()
        for post in posts:
            date = post['created_date']
            title = post['title']
            content = post['content']
            log.info('Date: {}, title; {}\n{}'.format(date, title, content))
        return blog
