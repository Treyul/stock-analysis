from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hashlib import sha512
from flask_login import UserMixin
db = SQLAlchemy()

# @login_manager.user_unauthorized
# def load_user(user_id):
#     return db.session.query(user).get(user_id)

# from app import manager

class user(db.Model, UserMixin):

    __tablename__ = "user"

    username = db.Column(db.String(255), primary_key=True,
                         unique=True, nullable=False)

    password = db.Column(db.Text(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_password(self, password):

        self.password = sha512(password.encode()).hexdigest()

    def check_password(self, password):

        provided_pass = sha512(password.encode()).hexdigest()

        # compare the passwords
        if provided_pass != self.password:
            return False
        elif provided_pass == self.password:
            return True
        else:
            return 404

    # @manager.user_loader
    # def load_user(user_id):
    #     return db.session.query(user).get(user_id)


class Stock(db.Model):

    __tablename__ = 'stocklogs'

    name = db.Column(db.String(50), primary_key=True,
                     unique=False, nullable=False)

    size_range = db.Column(db.JSON, nullable=False)

    colours = db.Column(db.JSON, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(db.JSON, nullable=False)
    test = db.Column(db.JSON, nullable=False)

    date = db.Column(db.DateTime(), default=datetime.utcnow())

    arrival_date = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, size_range, colours, amount, variation, date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.date = date


class SalesLog(db.Model):

    __tablename__ = "sales_logs"

    date_sold = db.Column(db.DateTime(), primary_key=True,
                          default=datetime.utcnow())

    sold_data = db.Column(db.JSON, nullable=False)

    no_of_sales = db.Column(db.Integer, nullable=False)

    def __init__(self, date_sold, sold_data, no_of_sales):

        self.date_sold = date_sold
        self.sold_data = sold_data
        self.no_of_sales = no_of_sales


class AvailableStock(db.Model):

    __tablename__ = "stock_available"

    name = db.Column(db.String(50), primary_key=True,
                     unique=True, nullable=False)

    size_range = db.Column(db.JSON, nullable=False)

    colours = db.Column(db.JSON, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(db.JSON, nullable=False)

    date = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)

    def __init__(self, name, size_range, colours, amount, variation, date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.date = date
