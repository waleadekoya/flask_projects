import os
import sys

git_ignore_template = '''
setup_instructions.txt
*.jpg
*.jpeg
*.png
__pycache__
*.pyc
*.pdf
instance/
'''
create_app_template = '''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from {0}_config import app_config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config['development'])
    db.init_app(db)
    
    migrate = Migrate(app, db)
    
    from {0}.admin.routes import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from {0}.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from {0}.home.routes import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    # add other blueprints here:
    
    db.create_all()

    return app
'''

run_app_template = '''
from {} import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
'''

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

</body>
</html>
'''

credentials_template = '''
def get_ip():
    import requests
    try:
        host_external_ip = requests.get('https://checkip.amazonaws.com').text.strip()
        return host_external_ip
    except Exception as e:
        print(e)
        
        
SECRET_KEY = 'p9Bv<3Eid9%$i01'
SQLALCHEMY_DATABASE_URI = f'mysql://your_username:your_password@' + str(get_ip()) + '/' + '{0}'
'''

config_template = '''
from instance import {0}_config


class BaseConfig:
    """Base config class"""
    SECRET_KEY = 'not_really_secret uh!?'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    """Production specific config"""
    SECRET_KEY = {0}_config.SECRET_KEY
    DEBUG = False


class StatingConfig(BaseConfig):
    """Staging specific config"""
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'not_really_secret?'
    SQLALCHEMY_DATABASE_URI = {0}_config.SQLALCHEMY_DATABASE_URI

 
app_config = dict(
    production=ProductionConfig,
    development=DevelopmentConfig,
    staging=StatingConfig
)

'''

route_template = '''
from flask import Blueprint, render_template

{0} = Blueprint(name='{0}', import_name=__name__)
'''

requirements_template = '''
flask
requests
flask-sqlalchemy
Flask-Migrate
flask_login
'''

models_template = '''
from {}.{} import db
'''


class MakeFlaskProjectDirectories:

    # The Divisional structure https://exploreflask.com/en/latest/blueprints.html

    def __init__(self, *, project_name: str,
                 app_name: str,
                 multi_model: bool = False,
                 model_names: list = None,
                 template_names: list = None,
                 static_files: bool = True,
                 modular_apps: bool = False,
                 modular_app_names: list = None):
        self.base_names = ['home', 'auth', 'admin']
        self.project_name = project_name
        self.app_name = app_name
        self.multi_model = multi_model
        self.model_names = model_names
        self.template_names = self.base_names if template_names is None \
            else list(set(template_names + self.base_names))
        self.static_files = static_files
        self.modular_apps = modular_apps
        self.modular_app_names = self.base_names if modular_app_names is None \
            else list(set(modular_app_names + self.base_names))
        self.dirname = os.path.dirname(__file__)
        self.project_dir = os.path.join(self.dirname, self.project_name)
        sys.path.insert(0, self.project_dir)
        print(sys.path)
        self.app_dir = os.path.join(self.dirname, self.project_name, self.app_name)
        self.modular_app_flag = self.modular_apps is True and self.modular_app_names is not None

        self.run()

    def run(self):
        try:
            self.create_project_dir()
            self.create_app_dir()
            self.generate_git_ignore_file()
            self.create_app_modules_folders()
            self.create_routes_files()
            self.create_forms()
            self.create_template_folder()
            self.create_template_files()
            self.create_static_folders()
            self.create_config_folders()
            self.create_config_files()
            self.create_init_file()
            self.create_setup_file()
            self.create_requirements_file()
            self.create_wsgi_file()
            self.create_models_folders()
            self.create_models_files()
            self.create_static_folders()
            self.create_static_files()
            self.create_start_sh()
        except OSError as e:
            print(e)

    @staticmethod
    def create_file(*args):
        open(os.path.join(*args), 'a')

    @staticmethod
    def create_dirs(*args):
        os.makedirs(*args, exist_ok=True)

    @staticmethod
    def write(file_path, content):
        with open(file_path, 'w+') as f:
            f.write(content)

    @staticmethod
    def get_ip():
        import requests
        try:
            host_external_ip = requests.get('https://checkip.amazonaws.com').text.strip()
            return host_external_ip
        except Exception as e:
            print(e)

    def create_project_dir(self):
        self.create_dirs(self.project_dir)

    def create_app_dir(self):
        self.create_dirs(self.app_dir)

    def generate_git_ignore_file(self):
        self.write(os.path.join(self.project_dir, '.gitignore'),
                   git_ignore_template)

    def create_template_folder(self):
        self.create_dirs(os.path.join(self.app_dir, 'templates'))
        if self.modular_app_flag:
            for app_name in self.modular_app_names:
                self.create_dirs(os.path.join(self.app_dir, 'templates', app_name))

    def create_template_files(self):
        self.write(os.path.join(self.app_dir, 'templates', 'base.html'),
                   html_template)
        if self.modular_app_flag:
            self.create_file(os.path.join(self.app_dir, 'templates', 'auth', 'login.html'))
            self.create_file(os.path.join(self.app_dir, 'templates', 'auth', 'register.html'))
            self.create_file(os.path.join(self.app_dir, 'templates', 'home', 'index.html'))
        else:
            if self.template_names is not None:
                for file_name in self.template_names:
                    html_file = str(file_name) + str('.html')
                    self.create_file(os.path.join(self.app_dir, 'templates', html_file))

    def create_static_folders(self):
        if self.static_files:
            self.create_dirs(os.path.join(self.app_dir, 'static'))
            self.create_dirs(os.path.join(self.app_dir, 'static', 'assets'))
            self.create_dirs(os.path.join(self.app_dir, 'static', 'css'))
            self.create_dirs(os.path.join(self.app_dir, 'static', 'js'))

    def create_static_files(self):
        if self.static_files:
            self.create_file(os.path.join(self.app_dir, 'static', 'css', 'main.css'))

    def create_init_file(self):
        self.write(os.path.join(self.app_dir, '__init__.py'),
                   create_app_template.format(self.app_name))
        self.write(os.path.join(self.project_dir, '__init__.py'),
                   create_app_template.format(self.app_name))

        if self.modular_app_flag:
            [self.create_file(os.path.join(self.app_dir, app_name, '__init__.py'))
             for app_name in self.modular_app_names]

    def create_app_modules_folders(self):
        if self.modular_app_flag:
            for app_name in self.modular_app_names:
                self.create_dirs(os.path.join(self.app_dir, app_name))

    def create_routes_files(self):
        if self.modular_app_flag:
            [self.write(os.path.join(self.app_dir, app_name, 'routes.py'),
                        route_template.format(app_name)) for app_name in self.modular_app_names]
        else:
            self.create_file(self.app_dir, 'routes.py')

    def create_forms(self):
        if self.modular_app_flag:
            [self.create_file(os.path.join(self.app_dir, app_name, 'forms.py'))
             for app_name in self.modular_app_names]
        else:
            self.create_file(self.app_dir, 'forms.py')

    def create_models_folders(self):
        if self.multi_model:
            self.create_dirs(os.path.join(self.app_dir, 'models'))

    def create_models_files(self):
        if self.multi_model:
            self.create_file(os.path.join(self.app_dir, 'models', '__init__.py'))
            if self.model_names is not None:
                for file_name in self.model_names:
                    python_file = str(file_name) + str('.py')
                    self.create_file(os.path.join(self.app_dir, 'models', python_file))
        else:
            self.write(os.path.join(self.app_dir, 'models.py'),
                       models_template.format(self.project_name, self.app_name))

    def create_config_folders(self):
        self.create_dirs(os.path.join(self.project_dir, 'instance'))

    def create_config_files(self):
        self.write(os.path.join(self.project_dir, 'instance',
                                '{}_config.py'.format(self.app_name)),
                   credentials_template.format(self.project_name))
        self.write(os.path.join(self.project_dir, '{}_config.py'.format(self.app_name)),
                   config_template.format(self.app_name))

    def create_setup_file(self):
        self.create_file(os.path.join(self.project_dir, 'setup.py'))

    def create_requirements_file(self):
        self.write(os.path.join(self.project_dir, 'requirements.txt'),
                   requirements_template)

    def create_wsgi_file(self):
        self.write(os.path.join(self.project_dir, 'wsgi.py'),
                   run_app_template.format(self.app_name))

    def create_start_sh(self):
        self.create_file(os.path.join(self.project_dir, 'start.sh'))


MakeFlaskProjectDirectories(project_name='my_app2',
                            app_name='some_app',
                            modular_apps=True,
                            modular_app_names=['test'])
