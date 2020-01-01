from flask import Flask
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

# initialise variable
# db = MongoEngine()
toolbar = DebugToolbarExtension()


def create_app():
    app = Flask(__name__)
    app.config.from_object('configuration.DevelopmentConfig')

    # initialise the toolbar debug extension
    toolbar.init_app(app)

    # initialise the database
    # db.init_app(app)

    # install bootstrap extension
    Bootstrap(app)

    with app.app_context():
        # include routes:
        from . import routes

        # register blueprints
        app.register_blueprint(routes.bp)

    return app
