
import os
import sys
import dotenv


class Config(object):

    FLASK_ENV = os.environ.get("FLASK_ENV")  
    FLASK_APP = os.environ.get("FLASK_APP")  
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = False



class TestConfig(Config):
    pass
class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True



class DevelopmentConfig(Config):
    pass


