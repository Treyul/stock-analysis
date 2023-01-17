from flask_mail import Mail, Message
import json
from flask import Flask, render_template, request, redirect, flash,session
from flask_cors import CORS
from sqlalchemy import ARRAY
from flask.cli import FlaskGroup

# import for database
from flask_migrate import Migrate, MigrateCommand
#  
from sqlalchemy import exc,or_
from pymysql import err
from pymysql import OperationalError


# imports for dates
from datetime import datetime
from datetime import date

# import for flask forms
from flask_wtf import CSRFProtect
from form import AddStock, Type_of_Stock, Sales, credentials, Login, CreateAccount,Multi
from flask_wtf import FlaskForm
from wtforms import BooleanField,SelectField, StringField, FormField, EmailField, SelectMultipleField, IntegerField, SubmitField, TextAreaField, PasswordField, FieldList,SearchField
from wtforms.validators import DataRequired, email, NumberRange


# import fro login config
from flask_login import UserMixin,LoginManager, login_user

# imports for destructuring json obj
from operator import itemgetter

# import for env variables
from os import getenv
# import for session management
# from flask_sessions import Session

# imports for mail
# TODO catch sql error for lost connection and force a retrial

# Define function to set json strings to Boolena values
def json_bool(value):
    if value == "False":
        return False
    else:
        return True

print(getenv("ST_KEY"))

app = Flask(__name__)

# config of packages
app.debug = True
app.config['SECRET_KEY'] = 'testing'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://b4efcd84e73da2:2d8fc5cf@us-cdbr-east-06.cleardb.net/heroku_4b7312ec17a7f3c"
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SESSION_PERMANENT']= False 
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)


cli = FlaskGroup(app)
manager = LoginManager()
manager.login_view = "login"
# manager = Manager(app)
# db = SQLAlchemy(app)
cli.add_command('db', MigrateCommand)

#  ******************** DATABASE MODELS imports   *********************
from model import *
migrate = Migrate(app, db)
db.init_app(app)

# db.create_all()
#   **********************  END OF DATABASE MODELS ************************


#   **************************  CREATE FORMS ********************************

class Wholesale(FlaskForm):

    product = StringField("Product name", validators=[DataRequired()], render_kw={"placeholder":"Item"})

    name = StringField("Shop name", validators=[DataRequired()], render_kw={"placeholder":"Shop no/Name"})

    size = IntegerField("size", validators=[DataRequired()], render_kw={"placeholder":"Size"})

    colour = StringField("Color",validators=[DataRequired()], render_kw={"placeholder":"Color"})

    # status = BooleanField("Status",default=False,render_kw={"placeholder":"Color"}) 

    paid = BooleanField("paid",default = False)

    add_sale = SubmitField("Add sale")


class salesform(FlaskForm):

    stock_sold = FieldList(FormField(Wholesale), min_entries=1)

    # Submit_data = SubmitField("Submit Sales Data") 

class Search(FlaskForm):

    string = SearchField("Enter what to search",render_kw={"placeholder":"Search"})

    submit = SubmitField("submit")


# ****************************END OF FORMS ***************************

# configuration of routes
@app.route("/",methods = ["POST","GET"])
def index():

    for i in range(3):
        try:
            products = AvailableStock.query.all()
            logs = Stock.query.all()
            sale = db.session.query(LocalSales).filter(or_(LocalSales.shop_no.like("test11"),LocalSales.shop_no.like(""))).all()
            # sale = LocalSales.query.filter_by(shop_no.like(""),shop_no.like("test8"))
            print(sale)
            print("*******")
            print(getenv("ST_KEY"))
            for log in logs:
                print(log.name)
            print(products,logs)
            for product in products:
                
                # convert json strings into objects
                product.size_range = json.loads(product.size_range)
                product.colours = json.loads(product.colours)
                # print(product.name)
                product.variation = json.loads(product.variation)
                # print(len(product.variation))
            return render_template("home.html",products = products)
        except (exc.DBAPIError,err.OperationalError,exc.SQLAlchemyError):
            pass 



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
    # TODO **last stocklog must be updated also so as to gt depletion date
    form = Type_of_Stock()
    Stock_log = Stock.query.filter_by(name="test1").all()
    print("here")
    print(Stock_log)

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

        stock_details = Stock(name=name, size_range=sizes, colours=colour, amount=amount, variation=variation, date=date.today())

        product = AvailableStock.query.filter_by(name=name).first()

        if not product:
            product = AvailableStock(name=name, size_range=sizes, colours=colour, amount=amount, variation=variation, date=date.today())

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
            product.date = date.today()
            
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

    # get current day sales


    day_sales = db.session.query(LocalSales).filter(LocalSales.date.like(f"%{date.today()}%")).all()
    day_sale = LocalSales.query.all()
    print(day_sales,date.today(),type(day_sale),day_sale[::-1])

    if day_sale:
        print("***********NOT EMPTY **************")

    

    if request.method == "POST":
        sales_data = request.get_json()
        print(sales_data)
        sold = 0

        # Ensure that stock data provided is correct
        # for poor connection retry 3 time then throw connection error to user
        for x in range(3):
            try:
                    for key in sales_data:

                        # check product exists
                        stock = AvailableStock.query.filter_by(name=key).first()
                        # print(stock.variation)

                        if not stock:
                            resp_msg = {"message": "error","error": f"The product {key} does not exist"}
                            return resp_msg

                        available_stock = json.loads(stock.variation)
                        available_sizes = json.loads(stock.size_range)
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

                                color = sold_color["color"]
                                shop = sold_color["name"]
                                # covert status and paid strings to boolean values
                                # status = sold_color["status"]
                                # if status == "false":
                                #     status = False
                                # elif status == "true":
                                #     status = True
                                status = False
                                paid = sold_color["paid"]
                                if paid == "false":
                                    paid = False
                                elif paid == "true":
                                    paid = True
                                print("tis",shop)

                                # Check if the color is available
                                if color not in old_color:
                                    resp_msg = {"message":"error","error":f"The colour {color} in size {size} not found"}
                                    return resp_msg

                                elif color in old_color:

                                    old_color[color] = old_color[color] - 1
                                    
                                    if old_color[color] < 0:
                                        resp_msg = {"message":"error","error":f"Cannot have negative stock amount"}
                                        return resp_msg
                                    # delete color if it is depeleted
                                    elif old_color[color] == 0:
                                        del old_color[color]

                                        # test also if stock size is depleted
                                        if len(old_color) == 0:
                                            del available_stock[size]

                                            # Update size lists
                                            available_sizes.remove(size)
                                            print(available_sizes)


                                        # test if the stock id depleted altogether
                                        if len(available_stock) == 0:
                                            AvailableStock.query.filter_by(name=key).delete()
                                            db.session.commit()
                                            print("****************************************")
                                            
                                            # Stock_log.depletion_date = date.today()
                                            db.session.commit()
                                            resp_msg = {"message":"success","success":f"The ${key} is depleted"}

                                            # print(SalesL)
                                            return resp_msg

                                    # TODO delete object from variation
                                    # elif old_color[color]  == 0
                                    #     return

                                    # upload sale to database
                                    sale = LocalSales(product=key,size=size,colour=color,shop_no=shop,paid=paid,status=status,date=date.today())

                                    db.session.add(sale)
                                    db.session.commit()

                                    # update available stock
                                    # TODO if amount is zero delete row
                                    # stock.amount = stock.amount - 1
                                    # stock.variation = json.dumps(available_stock)
                                    # stock.date = date.today()

                                        # TODO remove stock color and sizes and product altogether if depleted

                                    
                        sold = sold + amount_sold
                        # update stock amount remaining, variation, date
                        stock.amount = stock.amount - 1

                        # if stock.amount

                        stock.variation = json.dumps(available_stock)

                        stock.date = date.today()

                        stock.sizes = json.dumps(available_sizes)

                        db.session.commit()
                    
                    resp_msg = {"message":"success"}
                    # for key in sales_data:
                    sales_data =  json.dumps(sales_data)


                    return resp_msg
            except (exc.DBAPIError,err.OperationalError,exc.SQLAlchemyError):
                pass

                # if x == 3:
                #     resp_msg = {"message": "error","error": "PLease ensure you are connected to internet"}
                #     print("*************************CAUGHT*********************")
                #     return  resp_msg
                # else:
                #     continue


                

            # TODO check sold <= remaining


                    # for color in sold_color:

                    #     # catch error if color was not available
                    #     if color not in old_color:
                    #         resp_msg = {"message":"error","error":f"The colour {color} in size {size} not found"}
                    #         return resp_msg
                        
                    #     elif color in old_color:

                    #         old_color[color] = old_color[color] - sold_color[color]
                    #         amount_sold = amount_sold + sold_color[color]
                    #         print(f"summation for sold {sold}, {amount_sold}")

                    #         # catch error for negative entries
                    #         if old_color[color] < 0:
                    #             resp_msg = {"message":"error","error":f"Cannot have negative stock amount"}
                    #             return resp_msg

        # sales = SalesLog(date_sold=date.today(),
        #                  sold_data=sales_data, no_of_sales=sold)

        # db.session.add(sales)

        # db.session.commit()

    return render_template("record.html",form=Wholesale(),sales = day_sale[::-1])


@app.route("/test", methods=['GET', 'POST'])
def test():
    form = Search()

    # print("passes")

    if form.validate_on_submit():
        print("passed")
        print(form.is_submitted())

        product = form.product.data
        name = form.name.data
        size = form.size.data
        color = form.colour.data
        payment = form.paid.data
        status = form.status.data

        print(status,request.method)

    return render_template("test.html",form = form)
    
@app.route("/changepay",methods=["POST","GET"])
def changepay():

    if request.method == "POST":

        data = request.get_json() 

        name,size,colour,shop,ret,pay = itemgetter("name","size","colour","shop","return","pay")(data)
        ret = json_bool(ret)
        pay=json_bool(pay) 
 
        
        for i in range(3): 
            try: 
                # TODO For more accuracy add index
                sale = LocalSales.query.filter_by(product=name,size=size,colour=colour,shop_no=shop,status=ret,paid=pay).first()
                print(sale.index)
                sale.paid = not pay
                db.session.commit() 
                response_message = {"message":"success"}
                return response_message
            except (exc.DBAPIError,err.OperationalError,exc.SQLAlchemyError):
                continue
        
        # ret
            
@app.route("/changereturn",methods=["POST","GET"])
def changereturn():
    if request.method == "POST":

        response_message = {"message":"success","success":"successfully change status to return"}

        data = request.get_json()
        print(data)
        name,size,colour,shop,ret,pay = itemgetter("name","size","colour","shop","return","pay")(data)
        ret = json_bool(ret) 
        pay=json_bool(pay)
        print(ret,pay)
        for i in range(3):
            try:

                # set change into db and push it to remote db
                sale = LocalSales.query.filter_by(product=name,size=size,colour=colour,shop_no=shop,status=ret,paid=pay).first()
                
                if not sale:
                    response_message = {"message":"error","error":"There is an error with sale please refresh page"}
                    return response_message
                sale.status = not ret
                # db.session.commit() 

                # update available stock 
                stock = AvailableStock.query.filter_by(name=name).first()
                
                # if stock was depleted
                if not stock:

                    stock = AvailableStock(name=name,size_range=size,colours=colour,amount=1,variation=variation,date=date.today())

                    db.session.add(stock)
                    db.session.commit()

                    response_message = {"message":"success","success":"successfully change status to return"}
                
                variation = json.loads(stock.variation)
 
                # if size not available
                if not variation[size]:

                    size_var ={}
                    size_var[colour] = 1

                    variation[size] = size_var

                    # update variation
                    stock.variation = json.dumps(variation)

                    # update amount
                    stock.amount = stock.amount + 1

                    db.session.commit()

                    return response_message

                # else if color not available

                stock.amount = stock.amount + 1

                # oscillate through the stock variation to update it
                # get size variation
                # TODO catch error for stock,size,colour depletion
                size_var = variation[size]
                
                # if colour is not available 
                if not size_var[colour]:
                    size[colour] = 1 

                    stock.amount = stock.amount + 1

                    stock.variation = json.dumps(variation)

                    if colour not in json.loads(stock.colours):
                        colours = json.loads(stock.colours)
                        colours.append(colour)

                    db.session.commit()

                    return response_message
                

                # from the size variation get colour variation and update it
                size_var[colour] = size_var[colour] + 1

                print(variation)
                    # pass
                stock.variation = json.dumps(variation)

                # commit and push changes to db
                db.session.commit()
                response_message = {"message":"success","success":"successfully change status to return"}
                return response_message
            except (exc.DBAPIError,err.OperationalError,exc.SQLAlchemyError):
                return {"message":"error","error":"no internet"}
                # continue

            
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
    # cli()

    app.run(debug=True)

