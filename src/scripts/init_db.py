from flask import Flask
import __init__


from utils.database import DBAdapter

app = Flask(__name__)
with app.app_context():
    db = DBAdapter()

    db.init_db()
    db.create_user("admin","admin@gmail.com","123456")