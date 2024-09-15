from flask import Blueprint
from src.packages.auth.router import create_auth_blueprint
from src.packages.bookmarks.router import router as bookmarks_router


def create_api_blueprint(app):

    api = Blueprint("api",__name__)


    auth_router = create_auth_blueprint(app)
    api.register_blueprint(auth_router, url_prefix="/auth")




    api.register_blueprint(bookmarks_router, url_prefix="/bookmarks")



    @api.get("/")
    def index():
        return " API GATEWAY V1" 
    
    return api