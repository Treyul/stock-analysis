from django import forms
from datetime import date

class Retail_sales(forms.Form):

    product = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Product"}))
    
    size = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"size"}))
    
    colour = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"colour"}))
    
    name = forms.CharField(required=False,label="",widget=forms.TextInput(attrs={"placeholder":"shop"}))
    
    paid = forms.BooleanField(label="")
    
    buyer = forms.CharField( required=False,label="",widget=forms.TextInput(attrs={"placeholder":"buyer"}))
    
    amount = forms.IntegerField(label="",widget = forms.NumberInput(attrs={"placeholder":"Amount"}))
    

class Wholesale(forms.Form):

    product = forms.CharField(  label="",widget=forms.TextInput(attrs={"placeholder":"Item"}))

    name = forms.CharField( label="",widget=forms.TextInput(attrs={"placeholder":"Shop no/Name"}))

    size = forms.CharField(  label="",widget=forms.TextInput(attrs={"placeholder":"Size"}))

    colour = forms.CharField( label="",widget=forms.TextInput(attrs={"placeholder":"Color"}))

    paid = forms.BooleanField()

    # add_sale = SubmitField("Add sale")

class Search_sales(forms.Form):

    product = forms.CharField(label="",required=False, widget=forms.TextInput(attrs={"placeholder":"Product name"}))

    shop_number = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={"placeholder":"Shop no"}))

    size = forms.CharField(label = "", required=False,widget = forms.TextInput(attrs={"placeholder":"size"}))

    colour = forms.CharField(label="" ,required=False, widget = forms.TextInput(attrs = {"placeholder":"colour"}))

    paid = forms.CharField(label="paid", widget=forms.CheckboxInput())
    
    returned = forms.CharField(label="returned", widget=forms.CheckboxInput())
    
    start_date = forms.DateTimeField(required=False, widget = forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'})
        )
    
    # end_date = forms.DateField(required=False,widget=forms.DateInput())
    end_date = forms.DateTimeField(required=False, widget = forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date', "value":date.today()})
        )
    