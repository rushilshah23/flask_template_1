import datetime
from functools import wraps
from http import HTTPStatus
from flask import Flask, jsonify, make_response, redirect, request, url_for
import jwt

class JWTManager:

    def __init__(self,app):
        self.app:Flask = app

    def create_access_token(self,identity):
        payload = {
            "identity":identity,
            "exp":datetime.datetime.now(datetime.UTC) + self.app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }
        access_token = jwt.encode(payload,self.app.config['JWT_ACCESS_TOKEN_SECRET_KEY'],"HS256")
        return access_token
    
    def create_refresh_token(self,identity):
        payload = {
            "identity":identity,
            "exp":datetime.datetime.now(datetime.UTC) + self.app.config['JWT_REFRESH_TOKEN_EXPIRES']
        }
        refresh_token = jwt.encode(payload,self.app.config['JWT_REFRESH_TOKEN_SECRET_KEY'],"HS256")
        return refresh_token
    
    def verify_access_jwt_in_request(self):
        token = request.cookies.get('access_token')
        if not token:
            return False
        try:
            decoded_token = jwt.decode(token, self.app.config['JWT_ACCESS_TOKEN_SECRET_KEY'], algorithms=['HS256'])
            return decoded_token['identity']
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False


    def verify_refresh_jwt_in_request(self,token):
        # token = request.cookies.get('refresh_token')
        if not token:
            return False
        try:
            decoded_token = jwt.decode(token, self.app.config['JWT_REFRESH_TOKEN_SECRET_KEY'], algorithms=['HS256'])
            # return decoded_token['identity']
            return decoded_token

        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False


    def jwt_required(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            identity = self.verify_access_jwt_in_request()

            if not identity:
                # return redirect(url_for('render_admin_login'))
                return make_response(jsonify({"msg":"UnAuthenticated user"}), HTTPStatus.UNAUTHORIZED)

            return f(identity,*args, **kwargs)
        return decorated_function
    
    
    def refresh_token_about_to_expire(self,curr_refresh_token):
        exp = datetime.datetime.fromtimestamp(curr_refresh_token['exp'], datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        if exp - now <= self.app.config['JWT_REFRESH_TOKEN_RENEW_THRESHOLD']:
            return True
        else:
            return False

