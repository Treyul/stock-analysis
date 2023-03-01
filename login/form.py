from django import forms

# create user account form
# login form
class Login(forms.Form):

    username = forms.CharField(label="" ,widget=forms.TextInput( attrs={"placeholder": "username"}))

    password = forms.CharField(label="",widget=forms.PasswordInput( attrs={"placeholder": "password"}))
    
# form for account creation


class CreateAccount(forms.Form):

    name = forms.CharField(label="",widget=forms.TextInput( attrs={"placeholder": "Enter your name"}))

    username = forms.CharField(label="",widget=forms.TextInput( attrs={"placeholder":"Username"}))

    password = forms.CharField(label="",widget=forms.PasswordInput( attrs={"placeholder": "password"}))

    confirm_password = forms.CharField(label="",widget=forms.PasswordInput( attrs={"placeholder": "Confirm password"}))

    shop = forms.CharField(label="",widget = forms.TextInput(attrs={"placeholder":"Shop number"}))
    
    owner = forms.BooleanField("Are you the owner?")
    # email = EmailField("Email", validators = [Email(), DataRequired()])

# class New_user_form(UserCreationForm):
    