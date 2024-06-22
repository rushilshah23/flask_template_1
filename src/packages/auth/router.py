from flask import Blueprint, Flask, jsonify, make_response, request



def create_auth_blueprint(app:Flask):


    router = Blueprint("auth",__name__)
    

    @router.post("/login")
    def login_admin():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        user = app.db_adapter.get_user(username, password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401

        access_token =app.jwt_manager.create_access_token(identity={"username":username})
        refresh_token = app.jwt_manager.create_refresh_token(identity={"username":username})
        if access_token and refresh_token:
            resp = make_response(jsonify({"msg": "Login successful", "access_token":access_token,"refresh_token":refresh_token}))  # Provide a JSON response

            resp.set_cookie('access_token', 
                            access_token, 
                            httponly=True, 
                            secure=app.config['JWT_COOKIE_SECURE'],
                            max_age=app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
            resp.set_cookie('refresh_token', 
                            refresh_token, 
                            httponly=True, 
                            secure=app.config['JWT_COOKIE_SECURE'],
                            max_age=app.config['JWT_REFRESH_TOKEN_EXPIRES'].total_seconds())
            resp.status_code = 200  # Set the status code for redirection
            return resp
        return jsonify({"msg": "Login failed"}), 500

    @router.post("/logout")
    def admin_logout():
        resp = make_response(jsonify({"mssg":"Logout successfully"}))
        resp.delete_cookie("access_token")
        resp.delete_cookie("refresh_token")
        resp.status  = 200
        return resp


    @router.post("/refresh-token")
    def refresh_token():

        curr_refresh_token: str | None = request.cookies.get('refresh_token')
        if curr_refresh_token == None:
            curr_refresh_token = request.headers.get("refresh_token")
        
        

        decoded_curr_refresh_token = app.jwt_manager.verify_refresh_jwt_in_request(curr_refresh_token)
        if not decoded_curr_refresh_token:
            return jsonify({"msg":"Invalid refresh token"}), 401
        username = decoded_curr_refresh_token['identity']['username']
        # resp = make_response()
        new_access_token = app.jwt_manager.create_access_token(identity={"username":username})
        resp_data = {"access_token": new_access_token}
        # resp.set_cookie("access_token",new_access_token,httponly=True)
        # cheeck if refresh token is about to expire---
        if app.jwt_manager.refresh_token_about_to_expire(decoded_curr_refresh_token) == True:
            new_refresh_token = app.jwt_manager.create_refresh_token(identity={"username":username})
            resp_data['refresh_token'] = new_refresh_token

            resp = make_response(jsonify(resp_data))
            resp.set_cookie("refresh_token", new_refresh_token, httponly=True)
        else:
            resp = make_response(jsonify(resp_data))
        resp.set_cookie("access_token", new_access_token, httponly=True)

        return resp



    @router.get("/authenticate")
    def authenticate():
        pass

    return router