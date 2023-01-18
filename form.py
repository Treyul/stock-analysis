from flask_wtf import FlaskForm

from wtforms import HiddenField,SelectField, StringField, FormField, EmailField, SelectMultipleField, IntegerField, SubmitField, TextAreaField, PasswordField, FieldList

from wtforms.validators import DataRequired, email, NumberRange

from wtforms.widgets import ListWidget, CheckboxInput

# create checkboxs for multi-select fields


class Multi(SelectMultipleField):

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


# login form
class Login(FlaskForm):

    username = StringField("Name:", validators=[DataRequired()], render_kw={"placeholder": "username"})

    password = PasswordField("Paasword", validators=[DataRequired()], render_kw={"placeholder": "password"})
    
    Submit = SubmitField("Login")
# form for account creation


class CreateAccount(FlaskForm):

    name = StringField("Enter your full names", validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})

    # username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "password"})

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()], render_kw={"placeholder": "Confirm password"})

    # email = EmailField("Email", validators = [Email(), DataRequired()])

    Submit = SubmitField("Create account")


class AddStock(FlaskForm):

    name = StringField("Name of Stock", validators=[DataRequired()])

    size_range = StringField("size range of product",validators=[DataRequired()])

    colours = StringField("available colours", validators=[DataRequired()])

    Submit = SubmitField("Add new stalk")


class Type_of_Stock(FlaskForm):

    name = StringField("Name of stock: ", validators=[DataRequired()], render_kw={"placeholder": "Product name"})

    stock_type = SelectField(u'Type', choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")], validators=[DataRequired()], validate_choice=True)

    clothing = Multi("Size", choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")], validate_choice=True)

    max_size = IntegerField("max size: ",validators=[NumberRange(min=0, message="Cannot be less than 0")], render_kw={"placeholder": "Max Size"})

    min_size = IntegerField("min size: ",validators=[NumberRange(min=0, message="Cannot be less than 0")], render_kw={"placeholder": "min size"})

    interval = IntegerField("interval: ",validators=[NumberRange(min=0, message="Cannot be less than 0")], render_kw={"placeholder": "interval"})

    random = StringField("Random:" ,render_kw={"placeholder":"Random size"})
    
    colours = FieldList(StringField("Colour", validators=[DataRequired()], render_kw={"placeholder": "Colour"}), min_entries=1,)

    stock_data = HiddenField("Data: ", validators=[DataRequired()])

    add_stock = SubmitField("Add and Confirm stock")


class SalesData(FlaskForm):

    stock_type = SelectField(u'Type', choices=[('Clothes', 'Clothing'), ('Shoes', 'Shoes')], validators=[DataRequired()], validate_choice=True)

    stock_name = SelectField(u"Product Name", choices=[('Clothes', 'Clothing'), ('Shoes', 'Shoes')])

    colours = SelectField(u'Colour', choices=[('Clothes', 'Clothing'), ('Shoes', 'Shoes')])

    size = IntegerField("Size of product")

    no_sold = IntegerField("Number Sold")


class Sales(FlaskForm):

    stock_sold = FieldList(FormField(SalesData), min_entries=1)

    Submit_data = SubmitField("Submit Sales Data")


class credentials(FlaskForm):

    username = StringField("Name: ", validators=[DataRequired()])

    colours = FieldList("Colours", validators=[DataRequired()], min_entries=1)

    password = PasswordField("Password: ", validators=[DataRequired()])

    Submit = SubmitField("Submit")
