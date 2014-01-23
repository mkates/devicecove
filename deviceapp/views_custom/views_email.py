from django.shortcuts import render_to_response, redirect, render
from django.template.loader import render_to_string
from deviceapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

#### Renders and Sends the Email ##########
def render_and_send_email(template_data,subject,receiver):
	try:
		plaintext_context = Context(autoescape=False) # HTML escaping not appropriate in plaintext
		text_body = render_to_string("email_templates/test_plain.txt", template_data, plaintext_context)
		html_body = render_to_string("email_templates/email_template.html", template_data)
		msg = EmailMultiAlternatives(subject=subject, from_email="mhkates@gmail.com",to=[receiver], body=text_body)
		msg.attach_alternative(html_body, "text/html")
		msg.send()
		return 201
	except Exception,e:
		print e
		return 500
	
#### Welcome Email ######
def composeEmailWelcome(request,basicuser):
	template_data = {
		'welcome':True,
		'email_title':'Welcome',
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Welcome to VetCove!"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email
	
#### Partner Verification Program Confirmation #####
def composeEmailPVP(request,basicuser):
	template_data = {
		'pvp':True,
		'email_title':"PVP",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "You're VetCove Verified!"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email
	
#### Confirm Listing Was Posted ######
def composeEmailListingConfirmation(request,basicuser,item):
	template_data = {
		'listing_confirmation':True,
		'item':item,
		'email_title':"Listing Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Your VetCove listing is now live for "+item.name
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	

#### A seller has asked you a new question ######
def composeEmailNewQuestion(request,basicuser,question):
	template_data = {
		'new_question':True,
		'question':question,
		'email_title':"New Question",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "New Question from a buyer on your item: "+question.item.name
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	

#### When someone fills out the contact message ######
def composeEmailContactMessage_Seller(request,basicuser,contact_message):
	template_data = {
		'contactmessage_seller':True,
		'contact_message':contact_message,
		'email_title':"New Contact Request",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "A Vetcove buyer wants to schedule a viewing of your "+contact_message.item.name
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	


#### Post contact message, follow up for Seller ######
def composeEmailContactMessageFollowUp_Seller(request,basicuser):
	return
#### Post contact message, follow up for Seller ######
def composeEmailContactMessageFollowUp_Buyer(request,basicuser):
	return
	
#### Receipt for commission charged on an item ######
def composeEmailCommissionCharged(request,basicuser):
	commission_obj = Commission.objects.get(id=1)
	template_data = {
		'commission_charged':True,
		'commission_obj':commission_obj,
		'email_title':"Commission Payment Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Your receipt from VetCove"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	

	
#### Confirmation Item Sold to Seller ######
def composeEmailItemSold_Seller(request,basicuser):
	purchased_item = PurchasedItem.objects.get(id=1)
	item =  purchased_item.cartitem.item
	template_data = {
		'item_sold_seller':True,
		'purchased_item':purchased_item,
		'item':item,
		'email_title':"Commission Payment Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Your VetCove item sold! "+purchased_item.cartitem.item.name
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	


##### Confirmation Item Purchased to Buyer ######
def composeEmailItemPurchased_Buyer(request,basicuser):
	bu = request.user.basicuser
	checkout = Checkout.objects.get(id=1)
	purchased_items = checkout.purchaseditem_set.all()
	shipping_address = checkout.shipping_address
	template_data = {
		'purchase_confirmation':True,
		'purchased_items':purchased_items,
		'checkout':checkout,
		'totals':True,
		'shipping_address':shipping_address,
		'payment':checkout.getpayment,
		'email_title':"Commission Payment Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Purchase Receipt from VetCove"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	

#### Item has shipped - to Buyer ######
def composeEmailItemShipped_Buyer(request,basicuser):
	purchased_item = PurchasedItem.objects.get(id=1)
	item =  purchased_item.cartitem.item
	template_data = {
		'item_shipped_buyer':True,
		'purchased_item':purchased_item,
		'item':item,
		'email_title':"Item Shipped",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Your VetCove purchase has shipped: "+item.name
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	


#### Confirmation Item Shipped to Seller ######
def composeEmailItemShipped_Seller(request,basicuser):
	purchased_item = PurchasedItem.objects.get(id=1)
	item =  purchased_item.cartitem.item
	template_data = {
		'item_shipped_seller':True,
		'purchased_item':purchased_item,
		'item':item,
		'email_title':"Item Shipped",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Your VetCove shipping information for "+item.name+" has been upated"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	

#### Confirmation check has been mailed ######
def composeEmailPayoutCheckSent(request,basicuser):
	check_obj = CheckPayout.objects.get(id=1)
	purchased_items = check_obj.purchaseditem_set.all()
	payout_subtotal = 0
	for ui in purchased_items:
		payout_subtotal += ui.total
	commission = int(.09*payout_subtotal*100)/float(100)
	cc_fee = int(.03*payout_subtotal*100)/float(100)
	payout_total = payout_subtotal-commission-cc_fee
	template_data = {
		'payout_check_sent':True,
		'purchased_items': purchased_items,
		'check_obj':check_obj,
		'totals':True,
		'cc_fee':cc_fee,
		'pay_subtotal':payout_subtotal,
		'pay_total':payout_total,
		'commission':commission,
		'email_title':"Check Payment Sent",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Payment from VetCove is on its way to you"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	

#### Confirmation check has been mailed ######
def composeEmailPayoutBankSent(request,basicuser):
	bank_obj = BankPayout.objects.get(id=1)
	purchased_items = bank_obj.purchaseditem_set.all()
	payout_subtotal = 0
	for ui in purchased_items:
		payout_subtotal += ui.total
	commission = int(.09*payout_subtotal*100)/float(100)
	cc_fee = int(.03*payout_subtotal*100)/float(100)
	payout_total = payout_subtotal-commission-cc_fee
	template_data = {
		'payout_check_sent':True,
		'purchased_items': purchased_items,
		'check_obj':check_obj,
		'totals':True,
		'cc_fee':cc_fee,
		'pay_subtotal':payout_subtotal,
		'pay_total':payout_total,
		'commission':commission,
		'email_title':"Check Payment Sent",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Payment from VetCove is on its way to you"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	

#### Alert the seller they have no payment method set ######
def composeEmailNoPayment(request,basicuser):
	bu = request.user.basicuser
	unpaid_items = bu.purchaseditemseller.filter(paid_out=False)
	payout_subtotal = 0
	for ui in unpaid_items:
		payout_subtotal += ui.total
	commission = int(.09*payout_subtotal*100)/float(100)
	cc_fee = int(.03*payout_subtotal*100)/float(100)
	payout_total = payout_subtotal-commission-cc_fee
	template_data = {
		'no_payment':True,
		'totals':True,
		'cc_fee':cc_fee,
		'pay_subtotal':payout_subtotal,
		'pay_total':payout_total,
		'commission':commission,
		'purchased_items':unpaid_items,
		'email_title':"No Payment Method",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':bu.email
	}
	subject = "Attention required on VetCove to receive payment"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	


#### User updated their payment information ######
def composeEmailPayoutUpdated(request,basicuser):
	bu = request.user.basicuser
	if bu.payout_method == 'check':
		payout = bu.check_address
	elif bu.payout_method == 'bank':
		payout = bu.default_payout_ba
	else:
		return composeEmailNoPayment(request,basicuser)
	template_data = {
		'payout_updated':True,
		'payout_method':bu.payout_method,
		'payout':payout,
		'email_title':"Updated Payout Method",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':'Alex Kates'
	}
	subject = "Confirmation of payment preferences update"
	email = render_and_send_email(template_data,subject,'mkates@mit.edu')
	return email	
