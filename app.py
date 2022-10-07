import json
from flask import Flask, render_template , request, redirect, flash
from datetime import datetime
# import for database models
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ARRAY

from flask.cli import FlaskGroup

from flask_migrate import Migrate, MigrateCommand

# imports for forms
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField,PasswordField, FieldList,IntegerField,FormField

from wtforms.validators import DataRequired, Email

from form import AddStock,Type_of_Stock,Sales,credentials

# models
# from model import AvailableStock

# imports for mail
from flask_mail import Mail,Message
app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'testing'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user2:Treyul18@localhost/flask_jwt_auth"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True 
app.config["MAIL_USERNAME"] = "emmanuelryley55@gmail.com"
app.config["MAIL_DEFAULT_SENDER"] = "emmanuelryley55@gmail.com"
app.config["MAIL_PASSWORD"] = "Elwito18"

cli = FlaskGroup(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
cli.add_command('db', MigrateCommand)

from model import AvailableStock

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

db.create_all()

@app.route('/update', methods = ['GET','POST'])
def update():
    form = Type_of_Stock()
    # col = Stock.query.with_entities(Stock.colours).all()
    # print(col)
    # form.stock_sold.colours.choices = []

    if form.validate_on_submit():
        name = form.name.data

        var = json.loads(form.stock_data.data)

        sizes = []
        for size in var.keys():
            sizes.append(size)
        # print(type(json.loads(pass_word)))
        colour = form.colours.data

        amount = 0
        for col in var.values():
            for am in col.values():
                amount = amount +am

        stock_details = Stock(name=name,size_range=sizes,colours=colour,amount=amount,variation=var,date=datetime.utcnow())

        product = AvailableStock.query.filter_by(name = name).first()

        if not product:
            product = AvailableStock(name=name,size_range=sizes,colours=colour,amount=amount,variation=var,date=datetime.utcnow())

            db.session.add(product)

            db.session.commit()

        # print(stock_details)


        db.session.add(stock_details)

        db.session.commit()
    #     users = user.query.filter_by(username = user_name).first()

    #     if users:
    #         print("exist")
    #         return redirect('/update')

    #     users = user(username=user_name, password=pass_word)

    #     db.session.add(users)
    #     db.session.commit()
    #     print("added")
        
    #     flash("Message received", "success")
    

    return render_template("index.html",form = form)

@app.route("/sales",methods = ['POST', 'GET'])
def addStock():

    if request.method == "POST":
        sales_data = request.get_json()
        print(sales_data.keys())

        # Ensure that stock data provided is correct
        for key in sales_data:
            
            # check product exists
            stock = AvailableStock.query.filter_by(name = key).first()

            if not stock:
                resp_msg = {"message": "error","error":f"{key} does not exist"}
                return resp_msg

            available_stock = stock.variation
            sold_stock = sales_data[key]
            # TODO check size exists
            # TODO check colour exists
            # TODO check sold <= remaining
        resp_msg = {"messagee""success"}
        # for key in sales_data:

        sales = SalesLog(date_sold=datetime.utcnow(),sold_data=sales_data,no_of_sales=10)

        db.session.add(sales)

        db.session.commit()


    return render_template("record.html")

if __name__ == "__main__":
    # app.run()
    cli()