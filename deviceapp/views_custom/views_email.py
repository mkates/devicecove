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
import commission as commission
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
import random
import string

#### Renders and Sends the Email ##########
def render_and_send_email(template_data,subject,receiver):
	try:
		plaintext_context = Context(autoescape=False) # HTML escaping not appropriate in plaintext
		text_body = render_to_string("email_templates/email_template.txt", template_data, plaintext_context)
		html_body = render_to_string("email_templates/email_template.html", template_data)
		msg = EmailMultiAlternatives(subject, text_body, "The VetCove Team <info@vetcove.com>",[receiver])
		msg.attach_alternative(html_body, "text/html")
		#msg.send()
		return 201
	except Exception,e:
		print e
		return 500
	
#### Welcome Email ######
def composeEmailWelcome(request,basicuser):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'welcome':True,
		'email_title':'Welcome',
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Welcome to VetCove!"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email
	
#### Partner Verification Program Confirmation #####
def composeEmailPVP(request,basicuser):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'pvp':True,
		'email_title':"PVP",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "You're VetCove Verified!"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email
	
#### Confirm Listing Was Posted ######
def composeEmailListingConfirmation(request,basicuser,item):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'listing_confirmation':True,
		'item':item,
		'email_title':"Listing Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Your VetCove listing is now live for "+item.name
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### A seller has asked you a new question ######
def composeEmailNewQuestion(request,basicuser,question):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'new_question':True,
		'question':question,
		'email_title':"New Question",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "New Question from a buyer on your item: "+question.item.name
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### When someone fills out the contact message ######
def composeEmailContactMessage_Seller(request,seller,contact_message):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'contactmessage_seller':True,
		'contact_message':contact_message,
		'email_title':"New Contact Request",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':seller.name
	}
	subject = "A Vetcove buyer wants to schedule a viewing of your "+contact_message.item.name
	email = render_and_send_email(template_data,subject,seller.email)
	return email	

#### Post contact message, follow up for Seller ######
def composeEmailContactMessageFollowUp_Seller(contact_message,token):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'selling_reminder':True,
		'temp_base':"http://127.0.0.1:5000",
		'contact_message':contact_message,
		'token': token,
		'email_title':"Contact Message Follow Up",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':contact_message.item.user.name
	}
	subject = "How did it go? Were you able to sell: "+contact_message.item.name
	email = render_and_send_email(template_data,subject,contact_message.item.user.email)
	return email
		
#### Post contact message, follow up for Seller ######
def composeEmailContactMessageFollowUp_Buyer(request,basicuser):
	return
	
#### Receipt for commission charged on an item ######
def composeEmailCommissionCharged(request,basicuser,commission_obj):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'savings': commission.commissionSavings(commission_obj.item),
		'original_commission':commission.originalCommission(commission_obj.item),
		'commission_charged':True,
		'commission_obj':commission_obj,
		'email_title':"Commission Payment Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Your receipt from VetCove"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

	
#### Confirmation Item Sold to Seller ######
def composeEmailItemSold_Seller(request,basicuser,purchased_item):
	item =  purchased_item.cartitem.item
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'item_sold_seller':True,
		'purchased_item':purchased_item,
		'item':item,
		'email_title':"Commission Payment Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':purchased_item.seller.name
	}
	subject = "Your VetCove item sold! "+purchased_item.cartitem.item.name
	email = render_and_send_email(template_data,subject,purchased_item.seller.email)
	return email	


##### Confirmation Item Purchased to Buyer ######
def composeEmailItemPurchased_Buyer(request,basicuser,checkout):
	bu = request.user.basicuser
	purchased_items = checkout.purchaseditem_set.all()
	shipping_address = checkout.shipping_address
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'purchase_confirmation':True,
		'purchased_items':purchased_items,
		'checkout':checkout,
		'totals':True,
		'shipping_address':shipping_address,
		'payment':checkout.payment,
		'email_title':"Commission Payment Confirmation",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Purchase Receipt from VetCove"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### Item has shipped - to Buyer ######
def composeEmailItemShipped_Buyer(request,basicuser,purchased_item):
	item =  purchased_item.cartitem.item
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'item_shipped_buyer':True,
		'purchased_item':purchased_item,
		'item':item,
		'email_title':"Item Shipped",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Your VetCove purchase has shipped: "+item.name
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	


#### Confirmation Item Shipped to Seller ######
def composeEmailItemShipped_Seller(request,basicuser,purchased_item):
	item =  purchased_item.cartitem.item
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'item_shipped_seller':True,
		'purchased_item':purchased_item,
		'item':item,
		'email_title':"Item Shipped",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Your VetCove shipping information for "+item.name+" has been upated"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### Confirmation check has been mailed ######
def composeEmailPayoutCheckSent(basicuser,check_obj):
	purchased_items = check_obj.purchaseditem_set.all()
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'payout_check_sent':True,
		'purchased_items': purchased_items,
		'check_obj':check_obj,
		'totals':True,
		'payment':check_obj,
		'email_title':"Check Payment Sent",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Payment from VetCove is on its way to you"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### Confirmation check has been mailed ######
def composeEmailPayoutBankSent(basicuser,bank_obj):
	purchased_items = bank_obj.purchaseditem_set.all()
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'payout_bank_sent':True,
		'purchased_items': purchased_items,
		'bank_obj':bank_obj,
		'totals':True,
		'payment':bank_obj,
		'email_title':"Bank Account Payout Sent",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Payment from VetCove is on its way to you"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### Alert the seller they have no payment method set ######
def composeEmailNoPayment(basicuser):
	bu = basicuser
	unpaid_items = bu.purchaseditemseller.filter(paid_out=False)
	payment = commission.getStatsFromPurchasedItems(unpaid_items)
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'no_payment':True,
		'totals':True,
		'payment':payment,
		'purchased_items':unpaid_items,
		'email_title':"No Payment Method",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':bu.email
	}
	subject = "Attention required on VetCove to receive payment"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

def composeEmailPayoutFailed(basicuser,bank_obj):
	purchased_items = bank_obj.purchaseditem_set.all()
	payment = commission.getStatsFromPurchasedItems(purchased_items)
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'payout_failed':True,
		'purchased_items': purchased_items,
		'totals':True,
		'payment':payment,
		'email_title':"Bank Account Payout Failed",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Attention required on VetCove to receive payment"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### User updated their payment information ######
def composeEmailPayoutUpdated(basicuser):
	bu = basicuser
	if bu.payout_method == 'check':
		payout = bu.check_address
	elif bu.payout_method == 'bank':
		payout = bu.default_payout_ba
	else:
		return composeEmailNoPayment(basicuser)
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'payout_updated':True,
		'payout_method':bu.payout_method,
		'payout':payout,
		'email_title':"Updated Payout Method",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':basicuser.name
	}
	subject = "Confirmation of payment preferences update"
	email = render_and_send_email(template_data,subject,basicuser.email)
	return email	

#### Authorized Buyer ######
def composeEmailAuthorizedBuyer(item,buyer):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'authorized_buyer':True,
		'item':item,
		'email_title':"Buyer Authorization",
		'email_teaser':'NEEDS TO BE FINISHED',
		'email_name':buyer.name
	}
	subject = "You are now approved to buy "+item.name+" online"
	email = render_and_send_email(template_data,subject,buyer.email)
	return email

	



