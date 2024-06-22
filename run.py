from src import create_app


if __name__ == "__main__":
    app = create_app(env_mode="development")
    app.run(debug=True, host=app.config['HOSTNAME'], port=app.config['PORT'])


