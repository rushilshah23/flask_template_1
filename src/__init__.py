import os
import dotenv
from flask import Flask
from flask_cors import CORS

from src.packages.api.router import create_api_blueprint
from src.packages.app.router import create_web_app
from src.utils.database import DBAdapter
from src.utils.jwt_manager import JWTManager



dotenv.load_dotenv("./envs/.flaskenv")  


def load_env(env_mode):
    if env_mode == "development":
        dotenv.load_dotenv("./envs/.dev.env")
    elif env_mode == "production":
        dotenv.load_dotenv(".envs//.prod.env")
    elif env_mode == "testing":
        dotenv.load_dotenv("./envs/.test.env")
    else:
        raise Exception("Select a valid environment")
# def load_env(env_mode):
#     base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#     dotenv.load_dotenv(os.path.join(base_dir, "envs\\.flaskenv"))
#     print("Paths - ",os.path.join(base_dir,"envs\\.flaskenv"))
#     if env_mode == "development":
#         dotenv.load_dotenv(os.path.join(base_dir, "envs\\.dev.env"))
#     elif env_mode == "production":
#         dotenv.load_dotenv(os.path.join(base_dir, "envs\\.prod.env"))
#     elif env_mode == "testing":
#         dotenv.load_dotenv(os.path.join(base_dir, "envs\\.test.env"))
#     else:
#         raise Exception("Select a valid environment")

def create_app(env_mode = os.environ.get("FLASK_ENV")):

    # print("ENV MODE - ",env_mode)
    load_env(env_mode)
    from src.configs.env import DevelopmentConfig, ProductionConfig, TestConfig
    app = Flask(__name__, instance_relative_config=True)

    if env_mode == "development":
        app.config.from_object(DevelopmentConfig)
    elif env_mode == "production":
        app.config.from_object(ProductionConfig)
    elif env_mode == "testing":
        app.config.from_object(TestConfig)
    else:
        raise Exception("Select a valid environment")
    
    print(app.config.get("FLASK_ENV"))
    print(app.config.get("SECRET_KEY"))
    
    print(app.config.get("SESSION_COOKIE_SECURE"))


   
    app.config['JWT_COOKIE_SECURE'] = True  # Set to True in production with HTTPS
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True

    CORS(app)
    jwt_manager = JWTManager(app)
    db_adapter = DBAdapter(app.config.get("DB_URL"))


    app.jwt_manager = jwt_manager
    app.db_adapter = db_adapter


    app.url_map.strict_slashes = False

    api = create_api_blueprint(app)
    app.register_blueprint(api,url_prefix="/api/v1")


    web_app = create_web_app(app)
    app.register_blueprint(web_app,url_prefix="/")

    @app.teardown_appcontext
    def close_db_connection(exception):
        db_adapter.close_connection(exception)
    

    return app


