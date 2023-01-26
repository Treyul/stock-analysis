
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from hashlib import sha512
from flask_login import UserMixin
from datetime import date
# from app import login_manager

db = SQLAlchemy()

# class user(db.Model, UserMixin):

#     __tablename__ = "user"

#     username = db.Column(db.String(255), primary_key=True,unique=True, nullable=False)

#     Fullname = db.Column(db.String(255),nullable=False)

#     password = db.Column(db.Text(), nullable=False)

#     rights = db.Column(db.String(10), nullable=False,default="attendant")

#     shop = db.Column(db.String(20), nullable= False)

#     # Shop_attendants = db.Column()

#     def __init__(self, username, password,Fullname,rights,shop):
#         self.username = username
#         self.password = password
#         self.Fullname = Fullname
#         self.rights = rights
#         self.shop = shop


#     def create_password(self, password):

#         self.password = sha512(password.encode()).hexdigest()

#     def check_password(self, password):

#         provided_pass = sha512(password.encode()).hexdigest()

#         # compare the passwords
#         if provided_pass != self.password:
#             return False
#         elif provided_pass == self.password:
#             return True
#         else:
#             return 404

#     # @login_manager.user_loader
#     def load_user(username):
#         return db.session.query(user).get(username)

#     def get_id(self):
#         return self.username

class Stock(db.Model):

    __tablename__ = 'stocklogs'

    index = db.Column(db.Integer, index = True,primary_key = True, unique= True,nullable=False)

    name = db.Column(db.String(50), unique=False, nullable=False)

    size_range = db.Column(LONGTEXT, nullable=False)

    colours = db.Column(LONGTEXT, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(LONGTEXT, nullable=False)

    Shipper_name = db.Column(db.String(255),nullable=True)

    date = db.Column(db.Date(), default=date.today())

    depletion_date = db.Column(db.Date(),default= None)

    def __init__(self, name, size_range, colours, amount, variation, date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.date = date

class AvailableStock(db.Model):

    __tablename__ = "stock_available"

    name = db.Column(db.String(50), primary_key=True,unique=True, nullable=False)

    size_range = db.Column(LONGTEXT, nullable=False)

    colours = db.Column(LONGTEXT, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(LONGTEXT, nullable=False)

    date = db.Column(db.Date(), default=date.today(), nullable=False)

    price = db.Column(db.Integer,nullable = True)

    def __init__(self, name, size_range, colours, amount, variation, date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.date = date

    # function to return the worth of goods in stock
    def worth(self):
        return self.amount * self.price
    

class LocalSales(db.Model):

    __tablename__ = "wholesale_sales"

    index = db.Column(db.Integer, index = True,primary_key = True, unique= True,nullable=False)

    product = db.Column(db.String(50), nullable = False )

    size = db.Column(db.Integer, nullable = False)

    colour = db.Column(db.String(50), nullable = False)

    shop_no = db.Column(db.String(10),nullable = False)

    status = db.Column(db.Boolean, nullable = False )

    paid = db.Column(db.Boolean, nullable = False)

    date = db.Column(db.Date(), default= date.today(), nullable=False)

    price = db.Column(db.Integer, nullable=False)

    def __init__(self,product,size,colour,shop_no,status,paid,date,price):

        # self.index = index
        self.product = product
        self.size = size
        self.colour = colour
        self.shop_no = shop_no
        self.status = status
        self.paid = paid
        self.date = date
        self.price = price

class Ordered(db.Model):

    __tablename__ = "stock_ordered"

    index = db.Column(db.Integer, index = True,primary_key = True, unique= True,nullable=False)

    name = db.Column(db.String(50), unique=False, nullable=False)

    size_range = db.Column(LONGTEXT, nullable=False)

    colours = db.Column(LONGTEXT, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(LONGTEXT, nullable=False)

    order_price = db.Column(db.Integer,nullable=False)

    shipping_co = db.Column(db.String(100),nullable=True)

    comments = db.Column(LONGTEXT,nullable=True)

    order_date = db.Column(db.Date(), default=date.today())

    arrival_date = db.Column(db.Date(), nullable = True)


    def __init__(self, name, size_range, colours, amount, variation,order_price, order_date, arrival_date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.order_price = order_price
        self.order_date = order_date
        self.arrival_date = arrival_date


# table for retail sales
class RetailSales(db.Model):

    __tablename__   =  "retail_sales"

    index = db.Column(db.Integer, index = True,primary_key = True, unique= True,nullable=False)

    product = db.Column(db.String(50), nullable = False )

    size = db.Column(db.Integer, nullable = False)

    colour = db.Column(db.String(50), nullable = False)

    shop_no = db.Column(db.String(10),nullable = False)

    status = db.Column(db.Boolean, nullable = False )

    paid = db.Column(db.Boolean, nullable = False)

    buyer = db.Column(db.String(255),nullable= True)

    amount = db.Column(db.Integer,nullable = True)

    date = db.Column(db.Date(), default= date.today(), nullable=False)

    def __init__(self,product,size,colour,shop_no,status,paid,date):

        # self.index = index
        self.product = product
        self.size = size
        self.colour = colour
        self.shop_no = shop_no
        self.status = status
        self.paid = paid
        self.date = date
