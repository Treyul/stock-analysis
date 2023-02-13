from django import forms

class Retail_sales(forms.Form):

    product = forms.CharField("Product name",forms.TextInput(attrs={"placeholder":""}))
    
    size = forms.CharField("Product name",forms.TextInput(attrs={"placeholder":""}))
    
    colour = forms.CharField("Product name",forms.TextInput(attrs={"placeholder":""}))
    
    shop_no = forms.CharField("Product name",forms.TextInput(attrs={"placeholder":""}))
    
    paid = forms.BooleanField("paid",default = False)
    
    buyer = forms.CharField("Product name",forms.TextInput(attrs={"placeholder":""}))
    
    amount = forms.IntegerField("Product name",attrs={"placeholder":""})
    

class Wholesale(forms.Form):

    product = forms.CharField("Product name",  forms.TextInput(attrs={"placeholder":"Item"}))

    name = forms.CharField("Shop name",  forms.TextInput(attrs={"placeholder":"Shop no/Name"}))

    size = forms.CharField("size",  forms.TextInput(attrs={"placeholder":"Size"}))

    colour = forms.CharField("Color", forms.TextInput(attrs={"placeholder":"Color"}))

    paid = forms.BooleanField("paid",default = False)

    # add_sale = SubmitField("Add sale")
