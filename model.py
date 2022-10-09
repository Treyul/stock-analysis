from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class user(db.Model):

    __tablename__ = "user"

    username = db.Column(db.String(255),primary_key = True, unique = True, nullable = False)

    password = db.Column(db.Text(), nullable = False)


    def __init__(self,username,password):
        self.username = username
        self.password = password

class Stock(db.Model):

    __tablename__ = 'stocklogs'

    name = db.Column(db.String(50),primary_key = True, unique = False , nullable = False)

    size_range  = db.Column(db.JSON, nullable = False)

    colours = db.Column(db.JSON, nullable = False)

    amount = db.Column(db.Integer, nullable = False)

    variation = db.Column(db.JSON , nullable = False)

    date = db.Column(db.DateTime(), default = datetime.utcnow())

    arrival_date = db.Column(db.DateTime(), default = datetime.utcnow())

    def __init__(self,name, size_range, colours, amount, variation,date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.date = date

class SalesLog(db.Model):

    __tablename__ = "sales_logs"
    
    date_sold = db.Column(db.DateTime(), primary_key = True, default = datetime.utcnow())

    sold_data = db.Column(db.JSON, nullable = False)

    no_of_sales = db.Column(db.Integer, nullable = False)

    def __init__(self,date_sold,sold_data,no_of_sales):

        self.date_sold = date_sold
        self.sold_data = sold_data
        self.no_of_sales = no_of_sales


class AvailableStock(db.Model):

    __tablename__ = "stock_available"

    name = db.Column(db.String(50),primary_key = True, unique=True, nullable = False)

    size_range = db.Column(db.JSON,nullable= False)

    colours = db.Column(db.JSON,nullable = False)

    amount = db.Column(db.Integer, nullable =False)

    variation = db.Column(db.JSON, nullable = False)

    date = db.Column(db.DateTime(), default = datetime.utcnow(), nullable = False)

    def __init__(self,name,size_range,colours,amount,variation,date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.date = date