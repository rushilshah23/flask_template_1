from flask import Blueprint
from src.packages.auth.router import create_auth_blueprint



def create_web_app(app):
    web_app= Blueprint("web_app",__name__)


    auth_router = create_auth_blueprint(app)
    web_app.register_blueprint(auth_router, url_prefix="/auth")


    @web_app.get("/")
    def index():
        return " WEB APP V3" 
    
    return web_app