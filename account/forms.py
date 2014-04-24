from django import forms

class SignUpForm(forms.Form):
	firstname = forms.CharField()
	lastname = forms.CharField()
	username = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 
	reenterpassword = forms.CharField(widget=forms.PasswordInput) 
	referrer_id = forms.CharField(required=False)
	rememberme = forms.BooleanField(required=False)

class LoginForm(forms.Form):
	username = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 

class FeedbackForm(forms.Form):
	love = forms.CharField(widget = forms.Textarea)
	change = forms.CharField(widget = forms.Textarea)

class ReferralForm(forms.Form):
	emails = forms.CharField(widget = forms.Textarea)