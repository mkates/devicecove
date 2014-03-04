from django import forms

class ContactForm(forms.Form):
	name = forms.CharField(max_length = 50)
	email = forms.CharField(max_length = 50)
	message = forms.CharField(max_length = 50)