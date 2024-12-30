import os, secrets
from datetime import timedelta
import os


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDev(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'  # Required for the application to work
    SECRET_KEY = 'thisissecretkey'
    # Enable user tracking in Flask-Security
    SECURITY_TRACKABLE = True 
    SECURITY_PASSWORD_SALT = "thisissaltt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False   
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_DEFAULT_TIMEOUT = 15
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0


    DEBUG = True