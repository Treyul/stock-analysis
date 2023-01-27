from flask_wtf import FlaskForm

from wtforms import DateField,HiddenField,SelectField, StringField, FormField, EmailField, SelectMultipleField, IntegerField, SubmitField, TextAreaField, PasswordField, FieldList,BooleanField

from wtforms.validators import DataRequired, email, NumberRange

from wtforms.widgets import ListWidget, CheckboxInput

# create checkboxs for multi-select fields


class Multi(SelectMultipleField):

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


# login form
class Login(FlaskForm):

    username = StringField("Name:", validators=[DataRequired()], render_kw={"placeholder": "username"})

    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "password"})
    
    submit = SubmitField("Login")
# form for account creation


class CreateAccount(FlaskForm):

    name = StringField("Enter your full names", validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})

    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder":"Username"})

    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "password"})

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()], render_kw={"placeholder": "Confirm password"})

    shop = StringField("Shop number",validators=[DataRequired()],render_kw={"placeholder":"Shop number"})
    
    owner = BooleanField("Are you the owner?")
    # email = EmailField("Email", validators = [Email(), DataRequired()])

    Submit = SubmitField("Create account")


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


class Order_Form(FlaskForm):

    name = StringField("Name of stock: ", validators=[DataRequired()], render_kw={"placeholder": "Product name"})

    stock_type = SelectField(u'Type', choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")], validators=[DataRequired()], validate_choice=True)

    clothing = Multi("Size", choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")], validate_choice=True)

    max_size = IntegerField("max size: ",validators=[NumberRange(min=0, message="Cannot be less than 0")], render_kw={"placeholder": "Max Size"})

    min_size = IntegerField("min size: ",validators=[NumberRange(min=0, message="Cannot be less than 0")], render_kw={"placeholder": "min size"})

    interval = IntegerField("interval: ",validators=[NumberRange(min=0, message="Cannot be less than 0")], render_kw={"placeholder": "interval"})

    random = StringField("Random:" ,render_kw={"placeholder":"Random size"})
    
    colours = FieldList(StringField("Colour", validators=[DataRequired()], render_kw={"placeholder": "Colour"}), min_entries=1,)

    stock_data = HiddenField("Data: ", validators=[DataRequired()])

    Shipper = StringField("Shipper name",render_kw={"placeholder":"Shipper's name"})
    
    price = IntegerField("Order price",render_kw={"placeholder":"Order price"})
    
    arrival = DateField("date of arrival",validators=[DataRequired()])
    
    add_stock = SubmitField("Add Order")


class Retail_sales(FlaskForm):

    product = StringField("Product name",validators=[DataRequired()],render_kw={"placeholder":""})
    
    size = StringField("Product name",validators=[DataRequired()],render_kw={"placeholder":""})
    
    colour = StringField("Product name",validators=[DataRequired()],render_kw={"placeholder":""})
    
    shop_no = StringField("Product name",validators=[DataRequired()],render_kw={"placeholder":""})
    
    paid = BooleanField("paid",default = False)
    
    buyer = StringField("Product name",validators=[DataRequired()],render_kw={"placeholder":""})
    
    amount = IntegerField("Product name",validators=[DataRequired()],render_kw={"placeholder":""})
    

class Wholesale(FlaskForm):

    product = StringField("Product name", validators=[DataRequired()], render_kw={"placeholder":"Item"})

    name = StringField("Shop name", validators=[DataRequired()], render_kw={"placeholder":"Shop no/Name"})

    size = StringField("size", validators=[DataRequired()], render_kw={"placeholder":"Size"})

    colour = StringField("Color",validators=[DataRequired()], render_kw={"placeholder":"Color"})

    paid = BooleanField("paid",default = False)

    add_sale = SubmitField("Add sale")


class Search(FlaskForm):

    product = StringField("product", render_kw={"placeholder":"Product"})

    name = StringField("name",render_kw={"placeholder":"Enter shop"})

    size = StringField("size",render_kw={"placeholder":"Enter sizes"})

    colour = StringField("color",render_kw={"placeholder":"Colours"})

    submit = SubmitField("Submit")

