from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import views_email as email_view
from deviceapp.models import *
import json
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
			# If it's the only credit card, set is as the default
			if not bu.default_payment_cc:
				bu.default_payment_cc = new_card
				#If no payment method is set, make it the payment method
				if bu.payment_method == 'none':
					bu.payment_method = 'card'
				bu.save()
			return {'status':201,'card':new_card,'error':'None'} # Success
		return {'status':500,'error':'Card Already Saved'} # Card Already Saved
	except Exception,e:
		return {'status':500,'error':e} # Failure

#Helper method to see if the card hash already exists
@login_required
def doesCardExist(bu,hash):
	cards = bu.balancedcard_set.all();
	for card in cards:
		if card.cardhash == hash:
			return True
	return False	
	
######## Deleting a Credit Card ############################
# Removes all references to the BU, but card remains to view in things like
# purchase history
@login_required
def deleteBalancedCard(request,bc):
	bu = request.user.basicuser
	# Delete the card from Balanced.com
	balanced.configure(settings.BALANCED_API_KEY)
	card = balanced.Card.find(bc.card_uri)
	card.unstore()
	#Remove reference to basic user 
	bc.user = None
	bc.save()
	bu.default_cc = None
	bu.save()
	#Make another card the default
	other_cards = bu.balancedcard_set.all()
	if other_cards:
		bu.default_cc = other_cards[0]
		bu.save()
	return 201
	
	
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
		#If no bank accounts, make it the default
		if bu.default_payout_ba == None:
			bu.default_payout_ba = bankaccount
		if bu.default_payment_ba == None:
			bu.default_payment_ba = bankaccount
		#If no payment method is set, make it the payment method
		if bu.payment_method == 'none':
			bu.payment_method = 'bank'
		if bu.payout_method == 'none':
			bu.payout_method = 'bank'
			email_view.composeEmailPayoutUpdated(bu)
		bu.save()
		# See if user has a balanced account
		balanced.configure(settings.BALANCED_API_KEY)
		if bu.balanceduri:
			customer = balanced.Customer.find(bu.balanceduri)
		# If not, create a Balanced Customer and update BU Profile
		else:
			customer = balanced.Customer(name=bu.name,email=bu.email,phone=bu.phonenumber).save()
			bu.balanceduri = customer.uri
			bu.save()
		#Add bank account to the customer
		try:
			customer.add_bank_account(bankaccount.uri)
			bank_account = balanced.BankAccount.find(bankaccount.uri)
			#Verify the account for debiting it
			verification = bank_account.verify()
			if verification.confirm(1, 1).state != 'verified':
				return {'status':500,'bank':bankaccount,'error':'Unable to verify the bank account'}
			return {'status':201,'bank':bankaccount,'error':'None'}
		except Exception,e:
			return {'status':500,'bank':bankaccount,'error':e}
		return {'status':201,'bank':bankaccount,'error':'None'}
	return {'status':500,'error':'Bank Account Already Exists'}

#Helper method to see if the card hash already exists
@login_required
def doesBankAccountExist(bu,fingerprint):
	bas = bu.balancedbankaccount_set.all();
	for ba in bas:
		if ba.fingerprint == fingerprint:
			return True
	return False
		
@login_required
def makeDefaultBankAccount(bu,ba_object):
	bu.default_payout_ba = ba_object
	bu.save()
	return
	

##########################################################
######## Payment Preferences##############################
##########################################################

@login_required
def makeDefaultPayment(request,type,id):
	if type == 'card' and request.method=="POST":
		card = BalancedCard.objects.get(id=id)
		bu = request.user.basicuser
		# Security Check
		if card.user == bu:
			bu.payment_method = 'card';
			bu.default_payment_cc = card
			bu.save() 
	elif type == 'bank' and request.method=="POST":
		bank = BalancedBankAccount.objects.get(id=id)
		bu = request.user.basicuser
		# Security Check
		if bank.user == bu:
			bu.payment_method = 'bank';
			bu.default_payment_ba = bank
			bu.save() 
	return HttpResponseRedirect('/account/payment')

@login_required
def makeDefaultPayout(request,type,id):	
	if type == 'bank' and request.method=="POST":
		bank = BalancedBankAccount.objects.get(id=id)
		bu = request.user.basicuser
		# Security Check
		if bank.user == bu:
			bu.payout_method = 'bank';
			bu.default_payout_ba = bank
			bu.save() 
			email_view.composeEmailPayoutUpdated(bu)
	return HttpResponseRedirect('/account/payment')


@login_required
def accountDeletePayment(request,type,id):
	dp = deletePayment(request,type,id)
	if dp['status'] == 201:
		return HttpResponseRedirect('/account/payment')
		
@login_required
def deletePayment(request,type,id):	
	if type == 'card' and request.method=="POST":
		card = BalancedCard.objects.get(id=id)
		bu = request.user.basicuser
		# Security Check
		if card.user == bu:
			# First check if its the default
			if bu.default_payment_cc == card:
				# Are there other cards?, make one of them the default
				cards = request.user.basicuser.balancedcard_set.exclude(id=card.id)
				if cards:
					bu.default_payment_cc = cards[0]
				else: #No other cards, must check default payment maybe reset it
					bu.default_payment_cc = None
					if bu.payment_method == 'card':
						if bu.default_payment_ba:
							bu.payment_method = 'bank'
						else:
							bu.payment_method = 'none'
			bu.save()
			card.user = None
			card.save()
	elif type == 'bank' and request.method=="POST":
		bank = BalancedBankAccount.objects.get(id=id)
		bu = request.user.basicuser
		# Security Check
		if bank.user == bu:
			# First check if its the default
			if bu.default_payment_ba == bank:
				# Are there other bank accounts?, make one of them the default payment
				accounts = request.user.basicuser.balancedbankaccount_set.exclude(id=bank.id)
				if accounts:
					bu.default_payment_ba = accounts[0]
				else: #No other bank accounts, must check default payment maybe reset it
					bu.default_payment_ba = None
					if bu.payment_method == 'bank':
						if bu.default_payment_cc:
							bu.payment_method = 'card'
						else:
							bu.payment_method = 'none'
			if bu.default_payout_ba == bank:
				# Are there other bank accounts?, make one of them the default payout
				accounts = request.user.basicuser.balancedbankaccount_set.exclude(id=bank.id)
				if accounts:
					bu.default_payout_ba = accounts[0]
				else: #No other bank accounts, must check default payment maybe reset it
					bu.default_payout_ba = None
					if bu.payout_method == 'bank':
						bu.payout_method = 'none'
		bu.save()
		bank.user = None
		bank.save()
	return {'status':201}
	
##########################################################
######## Update Address ##################################
##########################################################
	

@login_required
def addMailingAddress(request):
	if request.method == "POST":
		bu = BasicUser.objects.get(user=request.user)
		name = request.POST['name']
		address_one = request.POST['address_one']
		address_two = request.POST.get('address_two','')
		city = request.POST['city']
		state = request.POST['state']
		zipcode = request.POST['zipcode']
		phonenumber = request.POST['phonenumber']
		useraddress = UserAddress(user=bu,name=name,address_one=address_one,address_two=address_two,city=city,state=state,zipcode=zipcode,phonenumber=phonenumber)
		useraddress.save()
		bu.payout_method = 'check'
		bu.check_address = useraddress
		bu.save()
		return HttpResponseRedirect('/account/payment')
	return HttpResponseRedirect('/account/payment')
	
@login_required
def setMailingAddress(request,addressid):
	address = UserAddress.objects.get(id=addressid)
	bu = BasicUser.objects.get(user=request.user)
	if request.method == "POST" and address.user == bu:
		bu.check_address = address
		bu.payout_method = 'check'
		bu.save()
	return HttpResponseRedirect('/account/payment')
	
@login_required
def deleteMailingAddress(request,addressid):
	address = UserAddress.objects.get(id=addressid)
	bu = BasicUser.objects.get(user=request.user)
	if request.method == "POST" and address.user == bu:
		if bu.check_address == address: #If its the default mailing address
			addresses = request.user.basicuser.useraddress_set.exclude(id=address.id)
			if addresses:
				bu.check_address = addresses[0]
			else:
				bu.check_address = None
				if bu.payout_method == 'check':
					if bu.default_payout_ba:
						bu.payout_method = 'bank'
					else:
						bu.payout_method = 'none'
		bu.save()
		address.user = None
		address.save()
		return HttpResponseRedirect('/account/payment')
	return HttpResponseRedirect('/account/payment')
	
	
	
	
	
	
		
		
		
			