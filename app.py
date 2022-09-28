from flask import Flask, render_template , request

from flask_sqlalchemy import SQLAlchemy


# class User ()

app = Flask(__name__)

db = SQLAlchemy(app)

class user(db.Model):

    __tablename__ = "user"

    username = db.Column(db.String(20),primary_key = True, unique = True)

    def __init__(self,username):
        self.username = username



# if __name__ == "__main__":