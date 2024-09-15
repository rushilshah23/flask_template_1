
from datetime import timedelta
import os
from .interface import IConfig


class Config(IConfig):
    def __init__(self):
        self.FLASK_ENV = os.environ.get("FLASK_ENV")  
        self.FLASK_APP = os.environ.get("FLASK_APP")
        self.HOSTNAME = os.environ.get("HOSTNAME")
        self.PORT = int(os.environ.get("PORT"))

        self.JWT_ACCESS_TOKEN_EXPIRES= timedelta(seconds=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES")))  
        self.JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES'))) 
        self.JWT_REFRESH_TOKEN_RENEW_THRESHOLD= timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_RENEW_THRESHOLD'))) 
        self.SECRET_KEY=os.environ.get("SECRET_KEY")
        self.JWT_ACCESS_TOKEN_SECRET_KEY=os.environ.get("JWT_ACCESS_TOKEN_SECRET_KEY")
        self.JWT_REFRESH_TOKEN_SECRET_KEY=os.environ.get("JWT_REFRESH_TOKEN_SECRET_KEY")
        self.SESSION_COOKIE_SECURE = False
        self.DB_URL = os.environ.get("DB_URL")

        # print(FLASK_ENV," - ",FLASK_APP," - ",HOSTNAME," - ",PORT," - ",JWT_ACCESS_TOKEN_EXPIRES," - ",JWT_REFRESH_TOKEN_EXPIRES)
