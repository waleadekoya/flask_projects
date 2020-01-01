from flask import (render_template, Blueprint, current_app,
                   request, session, flash, make_response)

from .models.post import Post
from .models.blog import Blog
from .utils.database import MongoDB
from .models.user import User

bp = Blueprint('home', __name__)


@bp.route('/')
def home_page():
    return render_template(template_name_or_list='home.html')


@bp.route('/login')
def login_template():
    return render_template(template_name_or_list='login.html')


@bp.route('/register')
def register_template():
    return render_template(template_name_or_list='register.html')


@bp.before_app_first_request
def initialise_database():
    MongoDB()


@bp.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.is_login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    context = dict(email=session['email'])
    return render_template(template_name_or_list='profile.html', **context)


@bp.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)
    context = dict(email=session['email'])
    return render_template(template_name_or_list='profile.html', **context)


@bp.route('/blogs/<string:user_id>')
@bp.route('/blogs')
def list_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_user_id(user_id)
    else:
        user = User.get_by_email(session['email'])
        print(user.email)
    blogs = user.get_blogs()
    if blogs is None:
        flash('no blog for this user')

    context = dict(blogs=blogs, email=user.email)
    return render_template(template_name_or_list='user_blogs.html', **context)


@bp.route('/posts/<string:blog_id>')
def list_posts(blog_id):
    blog = Blog.get_from_mongo(blog_id)
    posts = blog.get_posts()
    context = dict(posts=posts,
                   blog_title=blog.title,
                   blog_id=blog.id)
    return render_template(template_name_or_list='posts.html', **context)


@bp.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():

    if request.method == 'GET':
        return render_template(template_name_or_list='new_blog.html')

    else:
        user = User.get_by_email(session['email'])
        title = request.form['title']
        description = request.form['description']

        # user.create_new_blog(title=title,
        #                      description=description)
        Blog(title=title,
             author=user.email,
             description=description,
             author_id=user.id).save_to_mongo()
        return make_response(list_blogs(user_id=user.id))


@bp.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template(template_name_or_list='new_post.html',
                               blog_id=blog_id)
    else:
        user = User.get_by_email(session['email'])
        title = request.form['title']
        content = request.form['content']

        new_post = Post(title=title,
                        content=content,
                        author=user.email,
                        blog_id=blog_id)
        new_post.save_to_mongo()
        return make_response(list_posts(blog_id))
