from django import forms

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 
	referrer_id = forms.CharField(required=False)
	rememberme = forms.BooleanField(required=False)

class FeedbackForm(forms.Form):
	love = forms.CharField(widget = forms.Textarea)
	change = forms.CharField(widget = forms.Textarea)

class ReferralForm(forms.Form):
	emails = forms.CharField(widget = forms.Textarea)