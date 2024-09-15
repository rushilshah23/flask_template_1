# from sqlalchemy import create_engine


# engine = create_engine('sqlite:///example.db',echo=True)


# # ---------------------------------------

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String


# Base = declarative_base()


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     useername = Column(String)
#     password = Column(String)



# Base.metadata.create_all(engine)


# # ------------------------------------
# from sqlalchemy.orm import sessionmaker

# Session = sessionmaker(bind=engine)

# session = Session()





# -------------------------------------------------------


import os
import sqlite3
from flask import g
import bcrypt
from src.utils.logger import app_logger

class DBAdapter:
    def __init__(self, db_name:str):
        self.db_name = db_name

    def get_connection(self):
        if 'db' not in g:
            g.db = sqlite3.connect(self.db_name)
            g.db.row_factory = sqlite3.Row  # Set row factory to sqlite3.Row to get dict-like rows

        return g.db

    def close_connection(self, exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db(self):
        print("Curr dir - ",os.getcwd())
        with open("./src/scripts/init_db.sql", "r") as f:
            conn = self.get_connection()
            conn.executescript(f.read())
            conn.commit()
        print("Database initialized!")


    def delete_db(self):
        print("Curr dir - ",os.getcwd())
        os.unlink(self.db_name)
        # with open("./src/scripts/delete_db.sql", "r") as f:
        #     conn = self.get_connection()
        #     conn.executescript(f.read())
        #     conn.commit()
        # print("Database deleted!")

    def get_user(self, username, password):
        conn = self.get_connection()
        cur = conn.execute('SELECT * FROM USERS WHERE USERNAME = ?', (username,))
        user = cur.fetchone()

        if user is None:
            return None  # User not found
        user = dict(user)
        stored_password = user["PASSWORD"]  
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return user
        else:
            return None  # Password does not match
    
    def create_user(self, username, email, password):
        # Check if the user or email already exists
        if self.user_exists(username):
            app_logger.log_info(f"Username - {username} already exists")
            return False
        if self.email_exists(email):
            app_logger.log_info(f"Emai - {email} already exists")
            return False

        # Hash the password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = self.get_connection()
        try:
            # Use parameterized query to prevent SQL injection
            conn.execute("INSERT INTO USERS (USERNAME, EMAILID, PASSWORD) VALUES (?, ?, ?)", (username, email, hashed_password))
            app_logger.log_info(f"Username - {username} with emailID - {email} created successfully")
            conn.commit()
            return True  # Return True if user creation is successful
        except Exception as e:
            print(f"Error creating user: {e}")
            return False  # Return False if user creation fails

    def user_exists(self, username):
        conn = self.get_connection()
        cur = conn.execute("SELECT COUNT(*) FROM USERS WHERE USERNAME = ?", (username,))
        return cur.fetchone()[0] > 0

    def email_exists(self, email):
        conn = self.get_connection()
        cur = conn.execute("SELECT COUNT(*) FROM USERS WHERE EMAILID = ?", (email,))
        return cur.fetchone()[0] > 0






    def add_media(self, name, media_type, path, used_at):
        conn = self.get_connection()
        conn.execute("INSERT INTO MEDIA_MASTER (NAME, MEDIA_TYPE, PATH, USED_AT) VALUES (?, ?, ?, ?)",
                     (name, media_type, path, used_at))
        conn.commit()

    def get_all_media(self):
        conn = self.get_connection()
        cur = conn.execute("SELECT * FROM MEDIA_MASTER")
        return cur.fetchall()

    def get_media(self, media_id):
        conn = self.get_connection()
        cur = conn.execute("SELECT * FROM MEDIA_MASTER WHERE ID = ?", (media_id,))
        return cur.fetchone()

    def update_media(self, media_id, name, media_type, path, used_at):
        conn = self.get_connection()
        conn.execute("UPDATE MEDIA_MASTER SET NAME = ?, MEDIA_TYPE = ?, PATH = ?, USED_AT = ? WHERE ID = ?",
                     (name, media_type, path, used_at, media_id))
        conn.commit()

    def delete_media(self, media_id):
        conn = self.get_connection()
        conn.execute("DELETE FROM MEDIA_MASTER WHERE ID = ?", (media_id,))
        conn.commit()
