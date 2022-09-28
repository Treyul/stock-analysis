from flask import Flask, render_template , request, redirect, flash

# import for database models
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ARRAY

from flask.cli import FlaskGroup

from flask_migrate import Migrate, MigrateCommand

# imports for forms
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField,PasswordField

from wtforms.validators import DataRequired, Email

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'testing'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user2:Treyul18@localhost/flask_jwt_auth"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

cli = FlaskGroup(app)
# manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
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

    def __init__(self,name, size_range, colours, amount, variation):

        self.name = name
        self.size_range = size_range
        self.colours = colours
        self.amount = amount
        self.variation = variation

db.create_all()

class  credentials(FlaskForm):

    username = StringField("Name:", validators=[DataRequired()])

    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/update', methods = ['GET','POST'])
def update():
    # form = ContactForm()
    form = credentials()

    if form.validate_on_submit():
        user_name = form.username.data

        pass_word = form.password.data

        print(user_name,pass_word)

        users = user.query.filter_by(username = user_name).first()

        if not users:
            print("exist")
            return

        users = user(username=user_name, password=pass_word)

        db.session.add(users)
        db.session.commit()
        print("added")
        
        flash("Message received", "success")
        return redirect('/update')

    return render_template("index.html", form = form)

if __name__ == "__main__":
    # app.run()
    cli()