from django import forms

class Retail_sales(forms.Form):

    product = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Product"}))
    
    size = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"size"}))
    
    colour = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"colour"}))
    
    shop_no = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":""}))
    
    paid = forms.BooleanField()
    
    buyer = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":""}))
    
    amount = forms.IntegerField(label="",widget = forms.NumberInput(attrs={"placeholder":""}))
    

class Wholesale(forms.Form):

    product = forms.CharField(  label="",widget=forms.TextInput(attrs={"placeholder":"Item"}))

    name = forms.CharField( label="",widget=forms.TextInput(attrs={"placeholder":"Shop no/Name"}))

    size = forms.CharField(  label="",widget=forms.TextInput(attrs={"placeholder":"Size"}))

    colour = forms.CharField( label="",widget=forms.TextInput(attrs={"placeholder":"Color"}))

    paid = forms.BooleanField()

    # add_sale = SubmitField("Add sale")
