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

class NewAccountDetailsForm(forms.Form):
	name = forms.CharField()
	organization_type = forms.CharField()
	number_of_vets = forms.IntegerField()
	practice_size = forms.IntegerField()
	website = forms.CharField(required=False)
	large = forms.BooleanField(required=False)
	small = forms.BooleanField(required=False)
	mixed = forms.BooleanField(required=False)

class NewAccountAddressForm(forms.Form):
	address_one = forms.CharField()
	address_two = forms.CharField(required=False)
	city = forms.CharField()
	state = forms.CharField()
	zipcode = forms.CharField()
