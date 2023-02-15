# imports for exceptions
import logging
import traceback

# from flask_mail import Mail, Message
import json
from flask import Flask, render_template, request, redirect, flash,session
from flask_cors import CORS
from sqlalchemy import ARRAY
from flask.cli import FlaskGroup

# import for database
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import exc,or_,and_
from sqlalchemy.sql import functions,func
from pymysql import err
from pymysql import OperationalError


# imports for dates
from datetime import datetime
from datetime import date

# import for flask forms
from form import *
from flask_wtf import FlaskForm
from wtforms import   SubmitField,SearchField


# import fro login config
from flask_login import UserMixin,LoginManager, login_user,login_required,current_user

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


app = Flask(__name__)

# config of packages
app.debug = True
app.config['SECRET_KEY'] = 'testing'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://b4efcd84e73da2:2d8fc5cf@us-cdbr-east-06.cleardb.net/heroku_4b7312ec17a7f3c"
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 200
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_PERMANENT']= False 
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = '  # enter your email here
# app.config['MAIL_DEFAULT_SENDER'] =  # enter your email here
# app.config['MAIL_PASSWORD'] = 


cli = FlaskGroup(app)
# manager = LoginManager()
login_manager =LoginManager(app)
login_manager.login_view = "login"
# manager = Manager(app)
# mail = Mail(app)

#  ******************** DATABASE MODELS imports   *********************
from model import *
migrate = Migrate(app, db)
db.init_app(app)
cli.add_command('db', MigrateCommand)


#   **********************  END OF DATABASE MODELS ************************
class user(db.Model, UserMixin):

    __tablename__ = "user"

    username = db.Column(db.String(255), primary_key=True,unique=True, nullable=False)

    Fullname = db.Column(db.String(255),nullable=False)

    password = db.Column(db.Text(), nullable=False)

    rights = db.Column(db.String(10), nullable=False,default="attendant")

    shop = db.Column(db.String(20), nullable= False)

    # Shop_attendants = db.Column()

    def __init__(self, username, password,Fullname,rights,shop):
        self.username = username
        self.password = password
        self.Fullname = Fullname
        self.rights = rights
        self.shop = shop


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

    @login_manager.user_loader
    def load_user(username):
        return db.session.query(user).get(username)

    def get_id(self):
        return self.username
#         # return super().get_id()

# configuration of routes
@app.route("/",methods = ["POST","GET"])
@login_required
def index():

    for i in range(3):
        try:

            # Query database for available stock, odered stock and sale data
            products = AvailableStock.query.all()
            order_list = Ordered.query.filter(Ordered.arrival_date >= date.today()).all()
            print(order_list)

            # Convert Available stock json literal strings into JSON objects
            for product in products:
                product.size_range = json.loads(product.size_range)
                product.colours = json.loads(product.colours)
                product.variation = json.loads(product.variation)

            # Convert Ordered stock json literal strings into JSON objects
            for order in order_list:
                order.size_range = json.loads(order.size_range)
                order.colours = json.loads(order.colours)
                order.variation = json.loads(order.variation)
            return render_template("home.html",products = products, pending_order = order_list)
        except  exc.SQLAlchemyError:
            print("*************CAUGHT!!!   ************")
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
        print(sha512(form.password.data.encode()).hexdigest())
        print(user_cnt.check_password(form.password.data))

        # check if user exists and also if passwords match
        if user_cnt and user_cnt.check_password(form.password.data):
            # session["Logged_in"] = True
            login_user(user_cnt)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/createaccount", methods=["GET", "POST"])
def create():

    form = CreateAccount()
    print(form.validate_on_submit())
    if form.validate_on_submit():

        if form.password.data == form.confirm_password.data:

            # TODO catc error for none similar passwords
            try:
                username = form.username.data
            # print("run through")

                password = sha512(form.password.data.encode()).hexdigest()

                new_user = user(username=username, Fullname=form.name.data, password= password,rights=form.owner.data,shop=form.shop.data)

            # TODO catch error for duplicate users

                db.session.add(new_user)

                db.session.commit()
            except Exception as error:
                print(type(error).__name__)

        return redirect("/login")

    return render_template("login.html", form=form)


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    # TODO **last stocklog must be updated also so as to gt depletion date
    form = Type_of_Stock()
    Stock_log = Stock.query.filter_by(name="test1").all()
    print("here")
    print(Stock_log)

    # col = Stock.query.with_entities(Stock.colours).all()
    # print(col)
    # form.stock_sold.colours.choices = []
    print(request.method)
    print(form.is_submitted())
    print(form.validate())


    if form.is_submitted():
        print("here....")
        name = form.name.data

        var = json.loads(form.stock_data.data)
        variation = form.stock_data.data

        sizes = []
        for size in var.keys():
            sizes.append(size)
        # print(type(json.loads(pass_word)))
        sizes = json.dumps(sizes)
        colour = json.dumps(form.colours.data)
        print(colour,sizes)

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
@login_required
def addStock():

    # get current day sales
    day_sales = db.session.query(LocalSales).filter(LocalSales.date.like(f"%{date.today()}%")).all()
    day_sale = LocalSales.query.all()

    if request.method == "POST":
        sales_data = request.get_json()
        sold = 0

        # Ensure that stock data provided is correct
        # for poor connection retry 3 time then throw connection error to user
        for x in range(3):
            try:
                    for key in sales_data:

                        # check product exists
                        stock = AvailableStock.query.filter_by(name=key).first()

                        if not stock:
                            resp_msg = {"message": "error","error": f"The product {key} does not exist"}
                            return resp_msg
                        
                        # cange JSON strings to JSON obj
                        available_stock = json.loads(stock.variation)
                        available_sizes = json.loads(stock.size_range)
                        sold_stock = sales_data[key]
                        amount_sold = 0 

                        # check size exists
                        for size in sold_stock:

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
                                # covert paid string to boolean value
                                status = False
                                paid = sold_color["paid"]
                                if paid == "false":
                                    paid = False
                                elif paid == "true":
                                    paid = True

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

                                            # update db object
                                            stock.size_range = json.dumps(available_sizes)


                                        # test if the stock id depleted altogether
                                        if len(available_stock) == 0:
                                            AvailableStock.query.filter_by(name=key).delete()
                                            
                                            # Stock_log.depletion_date = date.today()
                                            db.session.commit()
                                            resp_msg = {"message":"success","success":f"The ${key} is depleted"}

                                            # print(SalesL)
                                            # return resp_msg

                                    # TODO delete object from variation
                                    # elif old_color[color]  == 0
                                    #     return

                                    # upload sale to database
                                    sale = LocalSales(product=key,size=size,colour=color,shop_no=shop,paid=paid,status=status,date=date.today(),price=stock.price)

                                    db.session.add(sale)
                                    db.session.commit()

                                        # TODO remove stock color and sizes and product altogether if depleted

                                    
                        # update stock amount remaining, variation, date
                        stock.amount = stock.amount - 1

                        # if stock.amount

                        stock.variation = json.dumps(available_stock)

                        stock.date = date.today()

                        print(available_sizes)
                        stock.sizes = json.dumps(available_sizes)

                        db.session.commit()
                    
                    resp_msg = {"message":"success"}
                    # for key in sales_data:
                    sales_data =  json.dumps(sales_data)


                    return resp_msg
            except Exception as error:
                print("****************CAUGHT!!!!!!**************")
                pass

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
@login_required
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
@login_required
def changereturn():
    if request.method == "POST":

        response_message = {"message":"success","success":"successfully change status to return"}

        data = request.get_json()

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

@app.route("/settings",methods=["POST","GET"])
@login_required
def settings():
    unpriced_stock = AvailableStock.query.filter_by(price=None).all()
    priced_stock = AvailableStock.query.filter(AvailableStock.price != None).all()
    attendants = user.query.filter_by(shop=current_user.shop).all()
    # print(unpriced_stock, priced_stock)

    # change json strings into json objects
    for stock in unpriced_stock:
        stock.size_range = json.loads(stock.size_range)
        stock.colours = json.loads(stock.colours)
        stock.variation = json.loads(stock.variation)
    for stock in priced_stock:
        stock.size_range = json.loads(stock.size_range)
        stock.colours = json.loads(stock.colours)
        stock.variation = json.loads(stock.variation)
    return render_template("settings.html",unpriced_stock=unpriced_stock,priced_stock=priced_stock)

@app.route("/retailsale",methods=["POST","GET"])
@login_required
def retailsale():
    Current_day_sales = db.session.query(RetailSales).filter(RetailSales.date == date.today()).all()
    return render_template("record.html",form=Retail_sales(),sales = Current_day_sales[::-1])

@app.route("/updateorder",methods=["POST","GET"])
@login_required
def updateorder():

    form = Order_Form()

    if form.is_submitted():
        name = form.name.data

        var = json.loads(form.stock_data.data)
        variation = form.stock_data.data

        sizes = []
        for size in var.keys():
            sizes.append(size)
        # print(type(json.loads(pass_word)))
        sizes = json.dumps(sizes)
        colour = json.dumps(form.colours.data)
        print(colour,sizes)

        amount = 0
        for col in var.values():
            for am in col.values():
                amount = amount + am

        stock_details = Ordered(name=name, size_range=sizes, colours=colour, amount=amount, variation=variation, order_price=form.price.data, order_date=date.today(), arrival_date=form.arrival.data)

        if form.Shipper.data:
            stock_details.shipping_co = form.Shipper.data

        db.session.add(stock_details)

        db.session.commit()
    return render_template("index.html",form= form)

@app.route("/analysis", methods=["POST","GET"])
@login_required
def analysis():

    # initilaize reponse
    response_message = {"message":"success"}
    # get current worth of stock in the shop
    Stock_worth = 0
    stock_available = AvailableStock.query.all()
    for stock in stock_available:
        Stock_worth = Stock_worth + stock.worth()

    # fetch current year analysis
    current_year_revenue = []
    current_year_volume = []

    # initialize start date to first day of january
    start = date.today().replace(month=1,day=1)

    for i in range(0,datetime.now().month):
        # get revenue and the no of sales for the month
        data = LocalSales.query.with_entities(functions.sum(LocalSales.price),functions.count()).filter(and_(LocalSales.date>=start,LocalSales.date < start.replace(month=i+2))).first()
        
        current_year_revenue.append(data[0])
        current_year_volume.append(data[1])

        start =  start.replace(month=i+2)
        
        # set current month values
        if datetime.now().month == start.month:
            current_revenue = data[0]
            current_volume = data[1]


    print(current_year_revenue,current_year_volume)
    # set dict value for the response message
    response_message["revenue"] = current_year_revenue
    response_message["volume"] = current_year_volume
    # send data to be rendered for graphs
    if request.method == "POST":
        print("passed")
        return response_message
        # Ordered.query.filter(Ordered.arrival_date >= date.today()).all()

        # pass
    # return {"message":"success","success":"successfully set price"}
    return render_template("analysis.html", worth=Stock_worth,revenue=current_revenue,volume=current_volume)

@app.route("/setprice", methods=["POST",])
@login_required
def setprice():
    if request.method == "POST":
        response = request.get_json()

        product_name = response["product"]
        new_price = response["price"]

        # fetch data from db
        product = AvailableStock.query.filter_by(name= product_name).first()

        # render error if product does not exist
        if not product:
            response_message = {"message":"error","error":"Cannot find product"}

        elif product:
            # set new price
            product.price = new_price

            # commit changes to db
            db.session.commit()
        
            response_message = {"message":"success","success":f"successfully set price to {new_price}"}
    return response_message

@app.route("/search",methods=["POST","GET"])
# @login_required
def search():

    if request.method == "POST":
        response = request.get_json()
        # print(response)
        shop_number = response["shop_no"]
        product_name = response["product"]
        shop_number,product_name = itemgetter("shop_no","product")(response)
        # size = response["size"]
        print(type((shop_number,product_name)))
        seeech={"shop_no":shop_number,"product":product_name}
        print(type(seeech))
        if shop_number:
            print(*seeech)
            sales = RetailSales.query.filter(or_(*seeech))
        # if product_name:
        #     sales = sales.filter(or_(RetailSales.product==product_name))

        # sales = []
        print(sales)

        # # Notify users when no results are found
        # if not sales:
        #     return {"message":"none","success":"No sales found"}
        # return {"message":"success","success":sales}
        return {"message":"success","success":"sales"}
    return render_template("search.html",form = Search())

# @app.route("/")
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
#     # app = create_app("config.py")
    # cli()

    app.run(debug=True)

