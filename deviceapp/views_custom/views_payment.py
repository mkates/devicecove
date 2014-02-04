from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import views_email as email_view
from deviceapp.models import *
import json, re, string
import datetime
from django.utils.timezone import utc
import balanced

##########################################################
######## Credit Cards ####################################
##########################################################

######## Adding a Credit Card ############################
# Must include all relevant post data in the request
# Success -> 201, Failure -> 500
# Returns status, card handle, and error
def addBalancedCard(request):
	uri = request.POST.get('uri','')
	brand = request.POST.get('brand','')
	cardhash = request.POST.get('hash','')
	expiration_month = request.POST.get('expiration_month','')
	expiration_year = request.POST.get('expiration_year','')
	last_four = request.POST.get('last_four','')
	try:
		# Configure Balanced API
		balanced.configure(settings.BALANCED_API_KEY)
		# Either find or get the Balanced Customer
		bu = BasicUser.objects.get(user=request.user)
		# See if user has a balanced account
		if bu.balanceduri:
			customer = balanced.Customer.find(bu.balanceduri)
		# If not, create a Balanced Customer and update BU Profile
		else:
			customer = balanced.Customer(name=bu.name,email=bu.email,phone=bu.phonenumber).save()
			bu.balanceduri = customer.uri
			bu.save()
		# If card not already saved, add the card to the customer and add the card to the database
		if not doesCardExist(bu,cardhash):
			customer.add_card(uri)
			new_card = BalancedCard(user=bu,uri=uri,brand=brand,cardhash=cardhash,expiration_month=expiration_month,expiration_year=expiration_year,last_four=last_four)
			new_card.save()
			if not bu.payment_method:
				bu.payment_method = new_card
				bu.save()
			return {'status':201,'card':new_card,'error':'None','balanceduri':bu.balanceduri} # Success
		return {'status':500,'error':'Card Already Saved'} # Card Already Saved
	except Exception,e:
		print e
		return {'status':500,'error':e} # Failure

# Helper method to see if the card hash already exists
@login_required
def doesCardExist(bu,hash):
	payments = bu.payment_set.all()
	for payment in payments:
		try: #Try block because payment could not be a balancedcard
			if payment.balancedcard and payment.balancedcard.cardhash == hash:
				return True
		except:
			i = 1 #Dummy variable
	return False	
		
##########################################################
######## Bank Accounts  ##################################
##########################################################
# The BA object is created on the client side
@login_required
def addBalancedBankAccount(request):
	bu = request.user.basicuser
	name = request.POST['name']
	uri = request.POST["uri"];
	fingerprint = request.POST["fingerprint"];
	bank_name = request.POST["bank_name"];
	bank_code = request.POST["bank_code"];
	account_number = request.POST["account_number"];
	if not doesBankAccountExist(bu,fingerprint):
		bankaccount = BalancedBankAccount(user=bu,name=name,uri=uri,fingerprint=fingerprint,bank_name=bank_name,bank_code=bank_code,account_number=account_number)
		bankaccount.save()
		# See if user has a balanced account
		balanced.configure(settings.BALANCED_API_KEY)
		if bu.balanceduri:
			customer = balanced.Customer.find(bu.balanceduri)
		# If not, create a Balanced Customer and update BU Profile
		else:
			customer = balanced.Customer(name=bu.name,email=bu.email,phone=bu.phonenumber).save()
			bu.balanceduri = customer.uri
			bu.save()
		# Add bank account to the customer
		try:
			customer.add_bank_account(bankaccount.uri)
			bank_account = balanced.BankAccount.find(bankaccount.uri)
			# Verify the account for debiting it
			verification = bank_account.verify()
			if verification.confirm(1, 1).state != 'verified':
				return {'status':500,'bank':bankaccount,'error':'Unable to verify the bank account'}
			if not bu.payment_method:
				bu.payment_method = bankaccount
			if not bu.payout_method:
				bu.payout_method = bankaccount
				email_view.composeEmailPayoutUpdated(bu)
			bu.save()
			return {'status':201,'bank':bankaccount,'error':'None','balanceduri':bu.balanceduri}
		except Exception,e:
			return {'status':500,'bank':bankaccount,'error':e}
	return {'status':500,'error':'Bank Account Already Exists'}

#Helper method to see if the card hash already exists
@login_required
def doesBankAccountExist(bu,fingerprint):
	payments = bu.payment_set.all()
	for payment in payments:
		try: #Try block because payment could not be a balancedcard
			if payment.balancedbankaccount and payment.balancedbankccount.fingerprint == fingerprint:
				return True
		except:
			i = 1 #Dummy variable
	return False

##########################################################
######## Payment Preferences##############################
##########################################################

@login_required
def makeDefaultPayment(request,id):
	payment = Payment.objects.get(id=id)
	bu = request.user.basicuser
	if payment.user == bu and request.method=="POST":
		bu.payment_method = payment
		bu.save()
	return HttpResponseRedirect('/account/payment')

@login_required
def makeDefaultPayout(request,id):	
	payment = Payment.objects.get(id=id)
	bu = request.user.basicuser
	if payment.user == bu and request.method=="POST":
		bu.payout_method = payment
		bu.save()
	return HttpResponseRedirect('/account/payment')

##### Gets all the payment objects of that type ####
def paymentObjectsOfType(bu,type):
	payments = bu.payment_set.all()
	p = []
	for payment in payments:
		if hasattr(payment,type):
			p.append(payment)
	return p
	
	
@login_required
def accountDeletePayment(request,id):
	deletePayment(request,id)
	return HttpResponseRedirect('/account/payment')		

@login_required
def deletePayment(request,id):
	payment = Payment.objects.get(id=id)
	bu = request.user.basicuser
	if payment.user == bu and request.method=="POST":
		payment.user = None
		payment.save()
		if bu.payment_method == payment:
			if paymentObjectsOfType(bu,'balancedcard'):
				bu.payment_method = paymentObjectsOfType(bu,'balancedcard')[0]
			elif paymentObjectsOfType(bu,'balancedbankaccount'):
				bu.payment_method = paymentObjectsOfType(bu,'balancedbankaccount')[0]
			else:
				bu.payment_method = None
			bu.save()
		if bu.payout_method == payment:
			if paymentObjectsOfType(bu,'balancedbankaccount'):
				bu.payout_method = paymentObjectsOfType(bu,'balancedbankaccount')[0]
			elif paymentObjectsOfType(bu,'balancedcheckaddress'):
				bu.payout_method = paymentObjectsOfType(bu,'balancedcheckaddress')[0]
			else:
				bu.payout_method = None
			bu.save()
	if hasattr(payment,'checkaddress'):
		payment.checkaddress.address.user = None
		payment.checkaddress.address.save()
	return 201
		
##########################################################
######## Update Address ##################################
##########################################################
	

@login_required
def addMailingAddress(request):
	if request.method == "POST":
		bu = request.user.basicuser
		name = request.POST['name']
		address_one = request.POST['address_one']
		address_two = request.POST.get('address_two','')
		city = request.POST['city']
		state = request.POST['state']
		zipcode = request.POST['zipcode']
		phonenumber = int(re.sub("[^0-9]", "",request.POST.get("phonenumber","")))
		useraddress = Address(user=bu,name=name,address_one=address_one,address_two=address_two,city=city,state=state,zipcode=zipcode,phonenumber=phonenumber)
		useraddress.save()
		#Every new mailing address is payout address object as well
		new_payment = CheckAddress(user=bu,address=useraddress)
		new_payment.save()
		if request.POST.get('payment',''):
			bu.payout_method = new_payment
			bu.save()
			return HttpResponseRedirect('/account/payment')
		else:
			return HttpResponseRedirect('/account/profile')
	return HttpResponseRedirect('/account/profile')
	
@login_required
def deleteMailingAddress(request,addressid):
	address = Address.objects.get(id=addressid)
	if request.method == "POST" and address.user == request.user.basicuser:
		deleteAddress(request,address)
		if request.POST.get('profile',''):
			return HttpResponseRedirect('/account/profile')
	return HttpResponseRedirect('/account/payment')
	
# Generic function to delete address, which also removes the payout objects
def deleteAddress(request,address):
	bu = request.user.basicuser
	for ca in CheckAddress.objects.filter(user=bu,address=address):
		if hasattr(bu.payout_method,'checkaddress'):
			if bu.payout_method.checkaddress.address != address: # only continue if not the payout address
				ca.user = None
				ca.save()
		else:
			ca.user = None
			ca.save()
	address.user = None
	address.save()
	return
	
		
		
		
			