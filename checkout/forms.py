from django import forms

class NewUserForm(forms.Form):
	firstname = forms.CharField(max_length=60)
	lastname = forms.CharField(max_length=60)
	email = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 
	zipcode = forms.IntegerField()
	checkout_signup = forms.BooleanField(required=False)