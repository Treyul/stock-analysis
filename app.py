from flask_mail import Mail, Message
import json
from flask import Flask, render_template, request, redirect, flash,session
from flask_cors import CORS
from sqlalchemy import ARRAY
from flask.cli import FlaskGroup

# import for database
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
from hashlib import sha512

# import for flask forms
from flask_wtf import CSRFProtect
from form import AddStock, Type_of_Stock, Sales, credentials, Login, CreateAccount
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FormField, EmailField, SelectMultipleField, IntegerField, SubmitField, TextAreaField, PasswordField, FieldList
from wtforms.validators import DataRequired, email, NumberRange


# import fro login config
from flask_login import UserMixin,LoginManager, login_user

# import for session management
# from flask_sessions import Session

# imports for mail

app = Flask(__name__)

# config of packages
app.debug = True
app.config['SECRET_KEY'] = 'testing'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://b4efcd84e73da2:2d8fc5cf@us-cdbr-east-06.cleardb.net/heroku_4b7312ec17a7f3c"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SESSION_PERMANENT']= False 
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)


cli = FlaskGroup(app)
manager = LoginManager()
manager.login_view = "login"
# manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cli.add_command('db', MigrateCommand)

#  ******************** DATABASE MODELS   *********************

class user(db.Model, UserMixin):

    __tablename__ = "user"

    username = db.Column(db.String(255), primary_key=True,unique=True, nullable=False)

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

    name = db.Column(db.String(50), primary_key=True, unique=False, nullable=False)

    size_range = db.Column(LONGTEXT, nullable=False)

    colours = db.Column(LONGTEXT, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(LONGTEXT, nullable=False)

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

    date_sold = db.Column(db.DateTime(), primary_key=True, default=datetime.utcnow(), nullable=False)

    sold_data = db.Column(LONGTEXT, nullable=False)

    no_of_sales = db.Column(db.Integer, nullable=False)

    def __init__(self, date_sold, sold_data, no_of_sales):

        self.date_sold = date_sold
        self.sold_data = sold_data
        self.no_of_sales = no_of_sales


class AvailableStock(db.Model):

    __tablename__ = "stock_available"

    name = db.Column(db.String(50), primary_key=True,
                     unique=True, nullable=False)

    size_range = db.Column(LONGTEXT, nullable=False)

    colours = db.Column(LONGTEXT, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(LONGTEXT, nullable=False)

    date = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)

    def __init__(self, name, size_range, colours, amount, variation, date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.date = date

class LocalSales(db.Model):

    __tablename__ = "wholesale_sales"

    product = db.Column(db.String(50),primary_key = True, nullable = False )

    size = db.Column(db.Integer, nullable = False)

    colour = db.Column(db.String(50), nullable = False)

    shop_no = db.Column(db.String(10),nullable = False)

    paid = db.Column(db.Boolean, nullable = False)

    def __init__(self,product,size,collour,shop_no,paid):

        self.product = product
        self.size = size
        self.colour = collour
        self.shop_no = shop_no
        self.paid = paid

class Ordered(db.Model):

    __tablename__ = "stock_ordered"

    name = db.Column(db.String(50), primary_key=True, unique=False, nullable=False)

    size_range = db.Column(LONGTEXT, nullable=False)

    colours = db.Column(LONGTEXT, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    variation = db.Column(LONGTEXT, nullable=False)

    order_date = db.Column(db.DateTime(), default=datetime.utcnow())

    arrival_date = db.Column(db.DateTime(), nullable = True)


    def __init__(self, name, size_range, colours, amount, variation, order_date, arrival_date):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation
        self.order_date = order_date
        self.arrival_date = arrival_date

# db.create_all()
#   **********************  END OF DATABASE MODELS ************************

# define decorator func to verify login
# def loginreq(func):

#     def required():
#         if not session.get("logged_in"):
#             return redirect("/login")
#         func()

#     return required


#   **************************  CREATE FORMS ********************************

class Wholesale(FlaskForm):

    product = StringField("Product name", validators=[DataRequired()])

    name = StringField("Shop name", validators=[DataRequired()])

    size = IntegerField("size", validators=[DataRequired()])

    colour = StringField("colur",validators=[DataRequired()])

    paid = StringField("paid",validators=[DataRequired()])



# ****************************END OF FORMS ***************************

# configuration of routes
@app.route("/",methods = ["POST","GET"])
def index():
    
    products = AvailableStock.query.all()
    print(products)
    for product in products:
        
        # convert json strings into objects
        product.size_range = json.loads(product.size_range)
        product.colours = json.loads(product.colours)
        product.variation = json.loads(product.variation)

    return render_template("home.html",products = products)


@app.route("/catalog", methods=['POST', 'GET'])
# @loginreq
def catalog():

    products = AvailableStock.query.all()
    print(products)
    for product in products:
        
        # convert json strings into objects
        product.size_range = json.loads(product.size_range)
        product.colours = json.loads(product.colours)
        product.variation = json.loads(product.variation)

    return render_template("catalog.html",products = products)


# route for logging in
@app.route("/login", methods=["GET", "POST"])
def login():

    form = Login()

    if form.validate_on_submit():

        # get user data
        user_cnt = db.session.query(user).filter(user.username == form.username.data).first()

        # check if user exists and also if passwords match
        if user_cnt and user_cnt.check_password(form.password.data):
            # session["Logged_in"] = True
            # login_user(user_cnt)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/createaccount", methods=["GET", "POST"])
def create():

    form = CreateAccount()
    if form.validate_on_submit():

        if form.password.data == form.confirm_password.data:

            # TODO catc error for none similar passwords
            username = form.name.data
            # print("run through")

            password = sha512(form.password.data.encode()).hexdigest()

            new_user = user(username=username, password= password)

            # TODO catch error for duplicate users

            db.session.add(new_user)

            db.session.commit()

        return redirect("/login")

    return render_template("login.html", form=form)


@app.route('/update', methods=['GET', 'POST'])
# @login_required
def update():
    form = Type_of_Stock()
    # col = Stock.query.with_entities(Stock.colours).all()
    # print(col)
    # form.stock_sold.colours.choices = []

    if form.validate_on_submit():
        name = form.name.data

        var = json.loads(form.stock_data.data)
        variation = form.stock_data.data

        sizes = []
        for size in var.keys():
            sizes.append(size)
        # print(type(json.loads(pass_word)))
        sizes = json.dumps(sizes)
        colour = json.dumps(form.colours.data)
        print(colour)

        amount = 0
        for col in var.values():
            for am in col.values():
                amount = amount + am

        stock_details = Stock(name=name, size_range=sizes, colours=colour, amount=amount, variation=variation, date=datetime.utcnow())

        product = AvailableStock.query.filter_by(name=name).first()

        if not product:
            product = AvailableStock(name=name, size_range=sizes, colours=colour, amount=amount, variation=variation, date=datetime.utcnow())

            db.session.add(product)

            db.session.commit()

        elif product:

            # revert variable back to array and objects
            sizes = json.loads(sizes)
            colour = json.loads(colour)
            # update stock available -- variation
            old_variation = json.loads(product.variation)
            old_sizes = json.loads(product.size_range)
            old_color = json.loads(product.colours)

            for size in old_variation:
                # Test for presence of size in new variation

                # If size is not in the newer stock
                if size not in var:
                    var[size] = old_variation[size]
                
                elif size in var:

                    # get old and new color variation for the size
                    old_colors = old_variation[size]
                    new_colors = var[size]

                    # test if there are new colors in the size
                    for color in old_colors:
                        
                        # insert color not present
                        if color not in new_colors:
                            new_colors[color] = old_colors[color]

                        # update the number of shoes
                        elif color in new_colors:
                            new_colors[color] = old_colors[color] + new_colors[color]
            product.variation = json.dumps(var)
            
            # update sizes
            print(sizes)
            for element in old_sizes:
                if element not in sizes:
                    sizes.append(element)
            product.size_range = json.dumps(sizes)
            print(sizes)

            # Update colours
            print(colour)
            for color in old_color:
                if color not in colour:
                    colour.append(color)
            print(colour)
            product.colours = json.dumps(colour)

            # update amount

            print(amount , product.amount)
            amount = amount + product.amount
            product.amount = amount

            #update time when stock was last updated
            product.date = datetime.utcnow()
            
            db.session.commit()

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

    return render_template("index.html", form=form)


@app.route("/sales", methods=['POST', 'GET'])
# @login_required
def addStock():

    if request.method == "POST":
        sales_data = request.get_json()
        sold = 0

        # Ensure that stock data provided is correct
        for key in sales_data:

            # check product exists
            stock = AvailableStock.query.filter_by(name=key).first()

            if not stock:
                resp_msg = {"message": "error",
                            "error": f"{key} does not exist"}
                return resp_msg

            available_stock = json.loads(stock.variation)
            # print(available_stock["23"])
            # print(available_stock[" 23"],"second")
            sold_stock = sales_data[key]
            amount_sold = 0

            # check size exists
            for size in sold_stock:

                # create var to store no sold
                # return error if size is not available in database
                if size not in available_stock:
                    resp_msg = {"message":"error","error":f"size {size} not found"}
                    return resp_msg

                elif size in available_stock:
                    # get size objects
                    old_color = available_stock[size]
                    sold_color = sold_stock[size]

                    for color in sold_color:

                        # catch error if color was not available
                        if color not in old_color:
                            resp_msg = {"message":"error","error":f"{color} in size {size} not found"}
                            return resp_msg
                        
                        elif color in old_color:

                            old_color[color] = old_color[color] - sold_color[color]
                            amount_sold = amount_sold + sold_color[color]
                            print(f"summation for sold {sold}, {amount_sold}")

                            # catch error for negative entries
                            if old_color[color] < 0:
                                resp_msg = {"message":"error","error":f"Cannot have negative stock amount"}
                                return resp_msg

                            # TODO remove stock color and sizes and product altogether if depleted

                           
            sold = sold + amount_sold
            # update stock amount remaining, variation, date
            stock.amount = stock.amount - amount_sold

            stock.variation = json.dumps(available_stock)

            stock.date = datetime.utcnow()

            db.session.commit()
                            
                            


                

            # TODO check sold <= remaining
        resp_msg = {"messagee""success"}
        # for key in sales_data:
        sales_data =  json.dumps(sales_data)

        sales = SalesLog(date_sold=datetime.utcnow(),
                         sold_data=sales_data, no_of_sales=sold)

        db.session.add(sales)

        db.session.commit()

    return render_template("record.html")



# def create_app(config_file):

#     # app = Flask(__name__)

#     CORS(app)

#     app.config.from_pyfile(config_file)
#     # app.config.from_file("config.py")

#     from model import db

#     # # loginm = LoginManager()
#     # cli = FlaskGroup(app)
#     # cli.add_command('db', MigrateCommand)


#     # @login_manager.user_loader
#     # def load_user(user_id):
#     #     return User.get(user_id)

#     # db.init_app(app)

#     csrf = CSRFProtect(app)

#     # Mail.init_app(app)

#     migrate.init_app(app,db)
#     import model
#     with app.app_context():
#         # loginm.init_app(app)
#         # cli.__init__(app)
#         csrf.init_app(app)
#         # loginm.add_command('db', MigrateCommand)
#         # db.create_all()

#     return app


if __name__ == "__main__":
    # app = create_app("config.py")
    cli()

#     app.run()

