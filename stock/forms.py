from django import forms

class Update_Available(forms.Form):

    name = forms.CharField(label="",  widget=forms.TextInput(attrs={"placeholder": "Product name"}))

    stock_type = forms.ChoiceField(label="", choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")])

    clothing = forms.CheckboxSelectMultiple( choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")])

    max_size = forms.IntegerField(label="", widget=forms.NumberInput(attrs={"placeholder": "Max Size"}))

    min_size = forms.IntegerField(label="", widget=forms.NumberInput(attrs={"placeholder": "min size"}))

    interval = forms.IntegerField(label="", widget=forms.NumberInput(attrs={"placeholder": "interval"}))

    random = forms.CharField(label="" ,widget=forms.TextInput(attrs={"placeholder":"Random size"}))
    
    # colours = forms.(forms.CharField(label="",  attrs={"placeholder": "Colour"}), min_entries=1,)

    stock_data = forms.HiddenInput( )

    # add_stock = SubmitField("Add and Confirm stock")


class Order_Form(forms.Form):

    name = forms.CharField(label="" ,  widget = forms.TextInput(attrs={"placeholder": "Product name"}))

    stock_type = forms.ChoiceField(label="" , choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")], )

    clothing = forms.CheckboxSelectMultiple( choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")],)

    max_size = forms.IntegerField(label="" , widget=forms.NumberInput(attrs={"placeholder": "Max Size"}))

    min_size = forms.IntegerField(label="" , widget=forms.NumberInput(attrs={"placeholder": "min size"}))

    interval = forms.IntegerField(label="" ,widget= forms.NumberInput(attrs={"placeholder": "interval"}))

    random = forms.CharField(label="" ,widget=forms.TextInput(attrs={"placeholder":"Random size"}))
    
    # colours = FieldList(forms.CharField("Colour",  attrs={"placeholder": "Colour"}), min_entries=1,)

    stock_data = forms.HiddenInput()

    Shipper = forms.CharField(label="" ,widget=forms.TextInput(attrs={"placeholder":"Shipper's name"}))
    
    price = forms.IntegerField(label="" ,widget=forms.NumberInput(attrs={"placeholder":"Order price"}))
    
    arrival = forms.DateField(label="" ,)
    
    # add_stock = SubmitField("Add Order")