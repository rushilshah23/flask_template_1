from flask import Flask
import __init__


from src import create_app
from src.utils.database import DBAdapter

app = create_app()
with app.app_context():
    db = DBAdapter(db_name=app.config.get("DB_URL"))

    db.init_db()
    db.create_user("admin","admin@gmail.com","123456")