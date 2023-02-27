from django import forms

class Retail_sales(forms.Form):

    product = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Product"}))
    
    size = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"size"}))
    
    colour = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"colour"}))
    
    name = forms.CharField(required=False,label="",widget=forms.TextInput(attrs={"placeholder":"Name"}))
    
    paid = forms.BooleanField()
    
    buyer = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Buyer Name"}))
    
    amount = forms.IntegerField(label="",widget = forms.NumberInput(attrs={"placeholder":"Amount"}))
    

class Wholesale(forms.Form):

    product = forms.CharField(  label="",widget=forms.TextInput(attrs={"placeholder":"Item"}))

    name = forms.CharField( label="",widget=forms.TextInput(attrs={"placeholder":"Shop no/Name"}))

    size = forms.CharField(  label="",widget=forms.TextInput(attrs={"placeholder":"Size"}))

    colour = forms.CharField( label="",widget=forms.TextInput(attrs={"placeholder":"Color"}))

    paid = forms.BooleanField()

    # add_sale = SubmitField("Add sale")
