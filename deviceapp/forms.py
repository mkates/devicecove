from django import forms

class NewUserForm(forms.Form):
	name = forms.CharField(max_length=60)
	email = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 
	zipcode = forms.IntegerField()
	checkout_signup = forms.BooleanField(required=False)

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 
	rememberme = forms.BooleanField(required=False)