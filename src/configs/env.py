
from datetime import timedelta
import os
import sys
import dotenv


class Config(object):

    FLASK_ENV = os.environ.get("FLASK_ENV")  
    FLASK_APP = os.environ.get("FLASK_APP")
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')))  
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES'))) 
    JWT_REFRESH_TOKEN_RENEW_THRESHOLD= timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_RENEW_THRESHOLD'))) 
    SECRET_KEY=os.environ.get("SECRET_KEY")
    JWT_ACCESS_TOKEN_SECRET_KEY=os.environ.get("JWT_ACCESS_TOKEN_SECRET_KEY")
    JWT_REFRESH_TOKEN_SECRET_KEY=os.environ.get("JWT_REFRESH_TOKEN_SECRET_KEY")
    SESSION_COOKIE_SECURE = False



class TestConfig(Config):
    pass
class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True



class DevelopmentConfig(Config):
    pass


