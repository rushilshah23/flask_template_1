
from flask import Flask
from flask_cors import CORS

from src.packages.api.router import create_api_blueprint
from src.packages.app.router import create_web_app
from src.utils.database import DBAdapter
from src.utils.jwt_manager import JWTManager


from src.configs import Config_Factory



def create_app():


    app = Flask(__name__, instance_relative_config=True)

    config_factory  = Config_Factory()
    configurations = config_factory.get_config()


    app.config.from_object(configurations)    

    print("--------CONFIG INFO----------------")
    print(app.config.get("FLASK_ENV"))
    print(app.config.get("SECRET_KEY"))
    
    print(app.config.get("SESSION_COOKIE_SECURE"))
    print(app.config.get("PORT"))
    print(app.config.get("HOSTNAME"))



   

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


