import os


import dotenv
from .interface import IConfig_Factory
from .base import Config
from .testing import TestConfig
from .production import ProductionConfig
from .development import DevelopmentConfig


class Config_Factory(IConfig_Factory):
    def get_config(self) :
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        envs_path = os.path.join(root_path,'envs')
        flask_env_path  = os.path.join(envs_path,".flaskenv")
        dotenv.load_dotenv(flask_env_path)

        env_mode = os.environ.get("FLASK_ENV")

        config_class   = None
        
        if env_mode == "development":
            env_file_path = os.path.join(envs_path,".dev.env")
            config_class =  DevelopmentConfig
        elif env_mode == "production":
            env_file_path = os.path.join(envs_path,"./.prod.env")
            config_class =   ProductionConfig
        elif env_mode == "testing":
            env_file_path = os.path.join(envs_path,"./.test.env")
            config_class =   TestConfig
        else:
            raise Exception("Select a valid environment")

        dotenv.load_dotenv(env_file_path)

        return config_class()
