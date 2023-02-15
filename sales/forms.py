from django import forms

class Retail_sales(forms.Form):

    product = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Product"}))
    
    size = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"size"}))
    
    colour = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"colour"}))
    
    shop_no = forms.CharField(widget=forms.TextInput(attrs={"placeholder":""}))
    
    paid = forms.BooleanField()
    
    buyer = forms.CharField(widget=forms.TextInput(attrs={"placeholder":""}))
    
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={"placeholder":""}))
    

class Wholesale(forms.Form):

    product = forms.CharField(  widget=forms.TextInput(attrs={"placeholder":"Item"}))

    name = forms.CharField( widget=forms.TextInput(attrs={"placeholder":"Shop no/Name"}))

    size = forms.CharField(  widget=forms.TextInput(attrs={"placeholder":"Size"}))

    colour = forms.CharField( widget=forms.TextInput(attrs={"placeholder":"Color"}))

    paid = forms.BooleanField()

    # add_sale = SubmitField("Add sale")
