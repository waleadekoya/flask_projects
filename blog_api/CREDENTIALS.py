
try:
    host = 'localhost'
except Exception as e:
    print(e)
    host = '81.140.200.10'

credentials = {
    'EMAIL_HOST_PASSWORD': 'omoyemi124',
    'PASSWORD': 'omoyemiHouse14+',
    'USER': 'wale',
    'PORT': '3306',
    'API_KEY': 'b1b7282c6165a7c85a00ea1d404db83e',
    'HOST': host,
    'EMAIL_HOST_USER': 'adekoya.wale@yahoo.com',
    'CELERY_BROKER_URL': 'amqp://wale:omoyemi123@localhost:5672/walevhost',
    'SQLAlchemy_Db_URI': 'mysql://wale:omoyemiHouse14+@{}'.format(host),
    'SECRET_KEY': 'special_secret_indeed?'
}