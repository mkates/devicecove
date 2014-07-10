from django import forms

###################################################
##### Sign Up and Log In Forms ####################
###################################################

class SignUpForm(forms.Form):
	username = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 
	confirmpassword = forms.CharField(widget=forms.PasswordInput) 
	referral_id = forms.CharField(required=False)
	promocode = forms.CharField(required=False)
	usertype = forms.CharField()

class LoginForm(forms.Form):
	username = forms.EmailField(max_length=60)
	password = forms.CharField(widget=forms.PasswordInput) 
	rememberme = forms.BooleanField(required=False)
	action = forms.CharField(required=False)

class NewAccountDetailsForm(forms.Form):
	name = forms.CharField()
	organization_type = forms.CharField()
	number_of_vets = forms.IntegerField()
	practice_size = forms.IntegerField()
	phonenumber = forms.CharField()
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

class NewAccountVerificationForm(forms.Form):
	practitioner_name = forms.CharField()
	license_no = forms.CharField()
	sales_no = forms.CharField(required=False)

class SupplierSignupForm(forms.Form):
	name = forms.CharField()
	primary_contact = forms.CharField()
	phonenumber = forms.CharField()
	address_one = forms.CharField()
	address_two = forms.CharField(required=False)
	city = forms.CharField()
	state = forms.CharField()
	zipcode = forms.CharField()
	website = forms.CharField()
	current_selling_method = forms.CharField()
	interest_listings = forms.BooleanField(required=False)
	interest_community = forms.BooleanField(required=False)
	interest_promotions = forms.BooleanField(required=False)
	interest_direct = forms.BooleanField(required=False)
	product_size = forms.CharField()
	referral_source = forms.CharField()
	
class FeedbackForm(forms.Form):
	love = forms.CharField(widget = forms.Textarea)
	change = forms.CharField(widget = forms.Textarea)

class ReferralForm(forms.Form):
	emails = forms.CharField(widget = forms.Textarea)


