import os
from blog_app import create_app

config_name = os.getenv('FLASK_CONFIG')


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
