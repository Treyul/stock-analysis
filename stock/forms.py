from django import forms


class ItemListForm(forms.Form):
    num_items = forms.IntegerField(widget=forms.HiddenInput())
    items = []

    def __init__(self, *args, **kwargs):
        num_items = kwargs.pop('num_items', 0)
        super().__init__(*args, **kwargs)

        for i in range(num_items):
            item_field = forms.CharField(required=False)
            self.fields[f'Colour {i+1}'] = item_field
            self.items.append(item_field)

    # def clean(self):
    #     cleaned_data = super().clean()
        # item_list_data = cleaned_data.get('item_list', [])
        # for i, item_data in enumerate(item_list_data):
        #     item_form = self.fields['item_list'].fields[i]
        #     item_form.cleaned_data = item_data
        #     if not item_form.is_valid():
        #         raise forms.ValidationError('Invalid item data')
        # return cleaned_data
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     item_list = cleaned_data.get('item_list', {})
    #     if isinstance(item_list, dict):
    #         item_list = item_list.get('item_list', [])
    #     cleaned_data['item_list'] = item_list
    #     return cleaned_data

class Update_Available(forms.Form):

    name = forms.CharField(label="",  widget=forms.TextInput(attrs={"placeholder": "Product name"}))

    stock_type = forms.ChoiceField(label="", choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")])

    clothing = forms.MultipleChoiceField(required=False,label="",widget=forms.CheckboxSelectMultiple(), choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")])

    max_size = forms.IntegerField(required=False,label="", widget=forms.NumberInput(attrs={"placeholder": "Max Size"}))

    min_size = forms.IntegerField(required=False,label="", widget=forms.NumberInput(attrs={"placeholder": "min size"}))

    interval = forms.IntegerField(required=False,label="", widget=forms.NumberInput(attrs={"placeholder": "interval"}))

    random = forms.CharField(required=False,label="" ,widget=forms.TextInput(attrs={"placeholder":"Random size"}))
    
    colours = ItemListForm(num_items=1)

    colour = forms.CharField(required=False, widget=forms.HiddenInput())

    stock_data = forms.CharField(required=False,widget=forms.HiddenInput() )

    # add_stock = SubmitField("Add and Confirm stock")


class Order_Form(forms.Form):

    name = forms.CharField(label="" ,  widget = forms.TextInput(attrs={"placeholder": "Product name"}))

    stock_type = forms.ChoiceField(label="" , choices=[('Alphabetic', 'Alphabetic'), ('Continuous', 'Continuous'),("intervaled","Intervaled"),("Random","Random")], )

    clothing = forms.MultipleChoiceField( label="",widget=forms.CheckboxSelectMultiple(),choices=[("3XS", "3XS"), ("2XS", "2XS"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("2XL", "2XL"), ("3XL", "3XL")],)

    max_size = forms.IntegerField(required=False,label="" , widget=forms.NumberInput(attrs={"placeholder": "Max Size"}))

    min_size = forms.IntegerField(required=False,label="" , widget=forms.NumberInput(attrs={"placeholder": "min size"}))

    interval = forms.IntegerField(required=False,label="" ,widget= forms.NumberInput(attrs={"placeholder": "interval"}))

    random = forms.CharField(required=False,label="" ,widget=forms.TextInput(attrs={"placeholder":"Random size"}))
    
    colours = ItemListForm(num_items=1)

    stock_data = forms.CharField(widget=forms.HiddenInput() )

    Shipper = forms.CharField(required=False,label="" ,widget=forms.TextInput(attrs={"placeholder":"Shipper's name"}))
    
    price = forms.IntegerField(required=False,label="" ,widget=forms.NumberInput(attrs={"placeholder":"Order price"}))
    
    arrival = forms.DateField(label="" ,)
    
    # add_stock = SubmitField("Add Order")