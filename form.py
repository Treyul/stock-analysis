from flask_wtf import FlaskForm

from  wtforms import SelectField,StringField,EmailField,SelectMultipleField,IntegerField, SubmitField, TextAreaField, PasswordField,FieldList

from wtforms.validators import Email, DataRequired

from wtforms.widgets import ListWidget,CheckboxInput


class Multi(SelectMultipleField):

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class credentials(FlaskForm):

    username = StringField("Name: ", validators = [DataRequired()])

    colours = FieldList("Colours", validators=[DataRequired()], min_entries=1)

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

class Type_of_Stock(FlaskForm):

    name = StringField("Name of stock: ", validators=[DataRequired()])

    stock_type = SelectField(u'Type',choices=[('Clothes','Clothing'),('Shoes','Shoes')], validators=[DataRequired()],validate_choice=True)

    clothing = Multi("Size",choices=[("XXXS","XXXS"),("XXS","XXS"),("XS","XS"),("S","S"),("M","M"),("L","L"),("XL","XL"),("XXL","XXL"),("XXXL","XXXL")],validate_choice=True)

    max_size = IntegerField("max size: ")

    min_size = IntegerField("min size: ")

    colours = FieldList(StringField("Colour", validators=[DataRequired()]), min_entries=1,)

    add_stock = SubmitField("Add and Confirm stock")

