import json
from flask import Flask, render_template , request, redirect, flash
from datetime import datetime
from flask_cors import CORS
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
from model import AvailableStock,db,user,SalesLog,Stock

# imports for mail
from flask_mail import Mail,Message
app = Flask(__name__)

# cli = FlaskGroup(app)
# migrate = Migrate(app, db)
# mail = Mail(app)
# cli.add_command('db', MigrateCommand)


app.route("/",methods = ['POST','GET'])
def index():

    return render_template("home.html")

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

def create_app(config_file):

    # app = Flask(__name__)

    CORS(app)

    app.config.from_pyfile(config_file,silent=True)

    from model import db

    db.init_app(app)

    # Mail.init_app(app)

    with app.app_context():
        db.create_all()
    

    return app

if __name__ == "__main__":
    app = create_app("config.py")

    app.run()

    # cli()