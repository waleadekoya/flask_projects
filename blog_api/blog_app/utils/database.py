__author__ = 'wale'

from typing import Union
import pymongo
from mysql.connector import connect, errorcode, Error, errors

from .logger import Logger
from CREDENTIALS import credentials

log = Logger().logger
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/


CNX_ERR_MSG = 'Access denied: user name and password is wrong.'
NO_DB_MSG = 'Database {} does not exist'
CXN_MSG = 'Database connection established...'
NEW_DB_MSG = 'Database "{}" created successfully.'
CREATE_DB_QUERY = "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8mb4'"
DB_FAILURE_MSG = 'Database creation failed: {}'
NEW_TBL_MSG = 'Creating table "{}": '
TBL_EXIST_MSG = '"{}" already exists.'


class MongoDB:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    def __init__(self):
        client = pymongo.MongoClient(MongoDB.URI)
        MongoDB.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection: str, data: dict):
        MongoDB.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Union[dict, list] = None):
        return MongoDB.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return MongoDB.DATABASE[collection].find_one(query)


class MySQLDb:

    def __init__(self):
        config = {
            'user': credentials.get('USER'),
            'password': credentials.get('PASSWORD'),
            'host': credentials.get('HOST'),
            'port': credentials.get('PORT'),
            'raise_on_warnings': True}
        try:
            self.connection = connect(**config)
            log.info(CXN_MSG)
        except Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.info(CNX_ERR_MSG)
            else:
                log.info(e)
        else:
            self.cursor = self.connection.cursor()

    def insert_record(self, query):
        try:
            self.cursor.execute(query)
        except errors.IntegrityError as e:
            log.info(e.msg)
            pass

    def run_query(self, query):
        self.cursor.execute(query)

    def create_db(self, db_name):
        try:
            self.cursor.execute(CREATE_DB_QUERY.format(db_name))
        except Error as e:
            log.info(DB_FAILURE_MSG.format(e))
            exit(1)

    def use_db(self, db_name):
        try:
            self.cursor.execute('USE {}'.format(db_name))
        except Error as e:
            if e.errno == errorcode.ER_BAD_DB_ERROR:
                log.info(NO_DB_MSG.format(db_name))
                self.create_db(db_name)
                log.info(NO_DB_MSG.format(db_name))
                self.connection.database = db_name
            else:
                log.info(e)
                exit(1)

    def create_table(self, table_name, query):
        try:
            self.cursor.execute(query)
            log.info(NEW_TBL_MSG.format(table_name))
        except Error as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                log.info(TBL_EXIST_MSG.format(table_name))
            else:
                log.info(e.msg)
