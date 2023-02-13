from django import forms

class Type_of_Stock(forms.Form):

    name = forms.CharField("Name of stock: ",  render_kw={"placeholder": "Product name"})

    stock_type = SelectField(u'Type', choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")],  validate_choice=True)

    clothing = Multi("Size", choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")], validate_choice=True)

    max_size = forms.IntegerField("max size: ", render_kw={"placeholder": "Max Size"})

    min_size = forms.IntegerField("min size: ", render_kw={"placeholder": "min size"})

    interval = forms.IntegerField("interval: ", render_kw={"placeholder": "interval"})

    random = forms.CharField("Random:" ,render_kw={"placeholder":"Random size"})
    
    colours = FieldList(forms.CharField("Colour",  render_kw={"placeholder": "Colour"}), min_entries=1,)

    stock_data = forms.HiddenInput("Data: ", )

    add_stock = SubmitField("Add and Confirm stock")


class Order_Form(forms.Form):

    name = forms.CharField("Name of stock: ",  render_kw={"placeholder": "Product name"})

    stock_type = SelectField(u'Type', choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")],  validate_choice=True)

    clothing = Multi("Size", choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")], validate_choice=True)

    max_size = forms.IntegerField("max size: ", render_kw={"placeholder": "Max Size"})

    min_size = forms.IntegerField("min size: ", render_kw={"placeholder": "min size"})

    interval = forms.IntegerField("interval: ", render_kw={"placeholder": "interval"})

    random = forms.CharField("Random:" ,render_kw={"placeholder":"Random size"})
    
    colours = FieldList(forms.CharField("Colour",  render_kw={"placeholder": "Colour"}), min_entries=1,)

    stock_data = forms.HiddenInput("Data: ", )

    Shipper = forms.CharField("Shipper name",render_kw={"placeholder":"Shipper's name"})
    
    price = forms.IntegerField("Order price",render_kw={"placeholder":"Order price"})
    
    arrival = DateField("date of arrival",
    
    add_stock = SubmitField("Add Order")