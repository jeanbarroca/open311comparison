import os

SECRET_KEY = 'thisismykey'
DEBUG = True

DB_USERNAME = 'jeanbarroca'
DB_PASSWORD = ''
DB_NAME = 'open311_comparison'
DB_HOST = os.getenv('IP','0.0.0.0')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

STATIC_FOLDER = '/home/ubuntu/workspace/open311_comparison/static'