from CREDENTIALS import credentials


class BaseConfig:
    """Base config class"""
    SECRET_KEY = 'not_really_secret uh!?'
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    """Production specific config"""
    SECRET_KEY = credentials.get('SECRET_KEY')
    DEBUG = False


class StatingConfig(BaseConfig):
    """Staging specific config"""
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'not_really_secret?'
