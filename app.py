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

from form import AddStock,Type_of_Stock

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

    size_range  = db.Column(db.String(10), nullable = False)

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

db.create_all()

@app.route('/update', methods = ['GET','POST'])
def update():
    # form = ContactForm()
    form = Type_of_Stock()

    if form.validate_on_submit():
        user_name = form.name.data

        pass_word = form.colours.data

        print(user_name,pass_word)

    #     c =form.colours.data
    #         # c.append(0)
    #     print(c)
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

@app.route("/addStock")
def addStock():

    form = AddStock()

    if form.validate_on_submit():
        return
    return

if __name__ == "__main__":
    # app.run()
    cli()