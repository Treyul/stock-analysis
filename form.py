from flask_wtf import FlaskForm

from  wtforms import StringField,EmailField, SubmitField, TextAreaField, PasswordField

from wtforms.validators import Email, DataRequired

class credentials(FlaskForm):

    username = StringField("Name: ", validators = [DataRequired()])

    password = PasswordField("Password: ", validators = [DataRequired()])

    Submit = SubmitField("Submit")

class AddStock(FlaskForm):

    name = StringField("Name of Stock",validators = [DataRequired()])

    size_range = StringField("size range of product", validators = [DataRequired()])

    colours = StringField("available colours", validators = [DataRequired()])

    Submit = SubmitField("Add new stalk")

class CreateAccount(FlaskForm):

    name = StringField("Enter your full names", validators= [DataRequired()])

    username = StringField("Username", validators = [DataRequired()])

    email = EmailField("Email", validators = [Email(), DataRequired()])

    Submit = SubmitField("Create account")