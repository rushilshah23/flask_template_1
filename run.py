from src import create_app
import dotenv

if __name__ == "__main__":
    # dotenv.load_dotenv("./envs/.flaskenv")  

    app = create_app()
    # app.run(debug=app.config['FLASK_ENV']!='production', host=app.config['HOSTNAME'], port=app.config['PORT'])
    app.run(debug=app.config['FLASK_ENV']!='production', host="0.0.0.0", port=app.config['PORT'])



