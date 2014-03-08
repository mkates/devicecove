from django.shortcuts import render_to_response, redirect, render
from django.template.loader import render_to_string
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
import random, string
from deviceapp.models import *
from questions.models import *
from helper.commission import *

######## Current Transcational Email List ############
# General: * Welcome, * PVP
# Pre-Sale: * Listing Confirmation, * Question Asked, * Contact Message, * Buy Authorization 
# Selling: * Order Confirmation, * Seller Item Sold
# Shipping: * Item Shipped, * Buyer Shipping Message 
# Payments: * Commission Charged, * No Payout, * Payout Failed, * Payout Sent
######################################################


#### Renders and Sends the Email ##########
def render_and_send_email(template_data,subject,receiver,email_path):
	try:
		plaintext_context = Context(autoescape=False) # HTML escaping not appropriate in plaintext
		text_body = render_to_string("email_templates/"+email_path+".txt", template_data, plaintext_context)
		html_body = render_to_string("email_templates/"+email_path+".html", template_data)
		html_body = html_body.replace("<a %a_style% ",'style="color: #2ba6cb; text-decoration: none;" ').replace("<p %p_style%",'<p style="color: #222222; font-family: "Helvetica", "Arial", sans-serif; font-weight: normal; text-align: left; line-height: 19px; font-size: 14px; margin: 0 0 10px; padding: 0;"')
		msg = EmailMultiAlternatives(subject, text_body, "The VetCove Team <info@vetcove.com>",[receiver])
		msg.attach_alternative(html_body, "text/html")
		if not hasattr(settings,'TESTING') and not hasattr(settings,'LOCAL'):
			msg.send()
		return {'template':"email_templates/"+email_path+".html",'data':template_data}
	except Exception,e:
		print e
		return 500

	
#### Welcome Email ######
def composeEmailWelcome(basicuser):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'actionrow':True,
		'email_title':'Welcome',
		'email_name':basicuser.firstname
	}
	subject = "Welcome to VetCove!"
	email = render_and_send_email(template_data,subject,basicuser.email,'welcome/welcome')
	return email
	
#### Partner Verification Program Confirmation #####
def composeEmailPVP(basicuser):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'actionrow': True,
		'email_title':"PVP",
		'email_name':basicuser.firstname
	}
	subject = "You're VetCove Verified"
	email = render_and_send_email(template_data,subject,basicuser.email,'pvp/pvp')
	return email
	
#### Confirm Listing Was Posted ######
def composeEmailListingConfirmation(basicuser,item):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'item':item,
		'email_title':"Listing Confirmation",
		'email_name':basicuser.firstname
	}
	subject = "Your VetCove listing is now live for "+item.name
	email = render_and_send_email(template_data,subject,basicuser.email,'listing_confirmation/listing_confirmation')
	return email	

#### A seller has asked you a new question ######
def composeEmailNewQuestion(basicuser,question):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'question':question,
		'email_title':"New Question",
		'email_name':question.seller.firstname
	}
	subject = "New Question from a buyer on your item: "+question.item.name
	email = render_and_send_email(template_data,subject,question.seller.email,'questions/questions')
	return email	

#### A seller has asked you a new question ######
def composeEmailQuestionAnswered(question):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'question':question,
		'email_title':"Answered Question",
		'email_name':question.buyer.firstname,
		'actionbutton':True,
		'actionbutton_link': 'http://www.vetcove.com/item/'+str(question.item.id)+"/details",
		'actionbutton_text': 'View This Item',
	}
	subject = "Answer to "+question.question
	email = render_and_send_email(template_data,subject,question.buyer.email,'questions/question_answered')
	return email

#### When someone fills out the contact message ######
def composeEmailContactMessage_Seller(seller,contact_message):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'contact_message':contact_message,
		'email_title':"New Contact Request",
		'email_name':seller.firstname
	}
	subject = "A Vetcove buyer wants to schedule a viewing of your "+contact_message.item.name
	email = render_and_send_email(template_data,subject,seller.email,'contact_message/contact_message')
	return email	

# #### Post contact message, follow up for Seller ######
# def composeEmailContactMessageFollowUp_Seller(contact_message,token):
# 	template_data = {
# 		'STATIC_URL':settings.STATIC_URL,
# 		'selling_reminder':True,
# 		'temp_base':"http://127.0.0.1:5000",
# 		'contact_message':contact_message,
# 		'token': token,
# 		'email_title':"Contact Message Follow Up",
# 		'email_teaser':'NEEDS TO BE FINISHED',
# 		'email_name':contact_message.item.user.name
# 	}
# 	subject = "How did it go? Were you able to sell: "+contact_message.item.name
# 	email = render_and_send_email(template_data,subject,contact_message.item.user.email)
# 	return email
		
# #### Post contact message, follow up for Seller ######
# def composeEmailContactMessageFollowUp_Buyer(request,basicuser):
# 	return
	
#### Receipt for commission charged on an item ######
def composeEmailCommissionCharged(basicuser,commission_obj):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'commission_obj':commission_obj,
		'two_col_row':True,
		'secondtextblock':True,
		'savings': commission.commissionSavings(commission_obj.item),
		'original_commission':commission.originalCommission(commission_obj.item),
		'email_title':"Commission Payment Confirmation",
		'email_name':basicuser.firstname
	}
	subject = "Your receipt from VetCove"
	email = render_and_send_email(template_data,subject,basicuser.email,'commission/commission')
	return email	

	
###### Confirmation Item Sold to Seller ######
def composeEmailItemSold_Seller(basicuser,purchased_item):
	item =  purchased_item.item
	actionbutton = True if purchased_item.shipping_included else False
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'purchased_item':purchased_item,
		'two_col_row':True,
		'secondtextblock':True,
		'actionbutton':actionbutton,
		'actionbutton_link': 'http://www.vetcove.com/account/sellhistory',
		'actionbutton_text': 'Enter shipping details / tracking number',
		'email_title':"Your Item Sold",
		'email_name':purchased_item.seller.firstname
	}
	subject = "Your VetCove item sold! "+purchased_item.item_name
	email = render_and_send_email(template_data,subject,purchased_item.seller.email,'item_sold/item_sold')
	return email	


##### Confirmation Item Purchased to Buyer ######
def composeEmailItemPurchased_Buyer(basicuser,order):
	bu = basicuser
	purchased_items = order.purchaseditem_set.all()
	shipping_address = order.shipping_address
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'purchase_confirmation':True,
		'purchaseditems':purchased_items,
		'order':order,
		'two_col_row':True,
		'totals':True,
		'shipping_address':shipping_address,
		'email_title':"Commission Payment Confirmation",
		'email_name':basicuser.firstname
	}
	subject = "Purchase Receipt from VetCove"
	email = render_and_send_email(template_data,subject,basicuser.email,'confirmation_receipt/confirmation_receipt')
	return email	

#### Item has shipped - to Buyer ######
def composeEmailItemShipped_Buyer(basicuser,purchased_item):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'item_shipped_buyer':True,
		'purchaseditem':purchased_item,
		'email_title':"Item Shipped",
		'email_name':purchased_item.buyer.firstname
	}
	subject = "Your VetCove purchase has shipped: "+purchased_item.item.name
	email = render_and_send_email(template_data,subject,purchased_item.buyer.email,'shipped/shipped')
	return email	

# #### Confirmation Item Shipped to Seller ######
# def composeEmailItemShipped_Seller(request,basicuser,purchased_item):
# 	item =  purchased_item.cartitem.item
# 	template_data = {
# 		'STATIC_URL':settings.STATIC_URL,
# 		'item_shipped_seller':True,
# 		'purchased_item':purchased_item,
# 		'item':item,
# 		'email_title':"Item Shipped",
# 		'email_teaser':'NEEDS TO BE FINISHED',
# 		'email_name':basicuser.name
# 	}
# 	subject = "Your VetCove shipping information for "+item.name+" has been upated"
# 	email = render_and_send_email(template_data,subject,basicuser.email)
# 	return email	

#### Confirmation check has been mailed ######
def composeEmailPayoutSent(basicuser,payout_obj):
	if hasattr(payout_obj,'bankpayout'):
		payout = payout_obj.bankpayout
	else:
		payout = payout_obj.checkpayout
	purchased_items = payout.purchaseditem_set.all()
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'payout_check_sent':True,
		'purchaseditems': purchased_items,
		'payout_obj':payout_obj,
		'payout':payout,
		'totals':True,
		'email_title':"Check Payment Sent",
		'email_name':basicuser.firstname
	}
	subject = "Payment from VetCove is on its way to you"
	email = render_and_send_email(template_data,subject,basicuser.email,'payout/payout_sent')
	return email	

#### Alert the seller they have no payment method set ######
def composeEmailNoPayment(basicuser):
	bu = basicuser
	unpaid_items = bu.purchaseditemseller.filter(paid_out=False)
	payment = commission.getStatsFromPurchasedItems(unpaid_items)
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'totals':True,
		'payout':True,
		'secondtextblock':True,
		'payout':payment,
		'purchaseditems':unpaid_items,
		'actionbutton':True,
		'actionbutton_link': 'http://www.vetcove.com/account/payment',
		'actionbutton_text': 'Update Payment Information',
		'email_title':"No Payment Method",
		'email_name':bu.firstname
	}
	subject = "Attention required on VetCove to receive payment"
	email = render_and_send_email(template_data,subject,basicuser.email,'payout/no_payout')
	return email	

def composeEmailPayoutFailed(basicuser,bank_account,eligibleitems):
	payment = commission.getStatsFromPurchasedItems(eligibleitems)
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'totals':True,
		'payout':True,
		'bank_account':bank_account,
		'secondtextblock':True,
		'payout':payment,
		'purchaseditems': eligibleitems,
		'actionbutton':True,
		'actionbutton_link': 'http://www.vetcove.com/account/payment',
		'actionbutton_text': 'Update Payment Information',
		'email_title':"Bank Account Payout Failed",
		'email_name':basicuser.firstname
	}
	subject = "Attention required on VetCove to receive payment"
	email = render_and_send_email(template_data,subject,basicuser.email,'payout/payout_failed')
	return email	

#### User updated their payment information ######
def composeEmailPayoutUpdated(basicuser):
	bu = basicuser
	if basicuser.payout_method:
		payout = basicuser.payout_method
	else:
		return composeEmailNoPayment(basicuser)
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'payout_updated':True,
		'payout':payout,
		'actionbutton':True,
		'actionbutton_link': 'http://www.vetcove.com/account/payment',
		'actionbutton_text': 'Update Payment Information',
		'email_title':"Updated Payout Method",
		'email_name':basicuser.firstname
	}
	subject = "Confirmation of payment preferences update"
	email = render_and_send_email(template_data,subject,basicuser.email,'payout/payout_updated')
	return email	

#### Authorized Buyer ######
def composeEmailAuthorizedBuyer(item,buyer):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'authorized_buyer':True,
		'item':item,
		'email_title':"Buyer Authorization",
		'actionbutton':True,
		'actionbutton_link': 'http://www.vetcove.com/item/'+str(item.id)+"/details",
		'actionbutton_text': 'Purchase Item',
		'email_name':buyer.firstname
	}
	subject = "You are now approved to buy "+item.name+" online"
	email = render_and_send_email(template_data,subject,buyer.email,'authorized_buyer/authorized_buyer')
	return email

#### Referral Email ######
def composeReferral(basicuser,email_list):
	template_data = {
		'STATIC_URL':settings.STATIC_URL,
		'referrer':basicuser,
		'referral_code':basicuser.referral_id,
		'email_title':str(basicuser.firstname)+" has invited you to the VetCove community",
		'actionbutton':True,
		'actionbutton_link': 'http://www.vetcove.com/referral/'+str(basicuser.referral_id),
		'actionbutton_text': 'Accept Invite'
	}
	subject = "Come explore the VetCove Community"
	for emails in email_list:
		email = render_and_send_email(template_data,subject,emails,'referral/referral')
	return email
	
def composeFileReport(report):
	plaintext_context = Context(autoescape=False) # HTML escaping not appropriate in plaintext
	text_body = render_to_string("email_templates/internal/reportfiled.txt", {'report':report}, plaintext_context)
	msg = EmailMultiAlternatives("VetCove Report Complaint", text_body, "The VetCove Team <info@vetcove.com>",[
	"mitch@vetcove","alex@vetcove.com"])
	msg.send()
	return

def composeInactiveRequest(inactiverequest):
	plaintext_context = Context(autoescape=False) # HTML escaping not appropriate in plaintext
	text_body = render_to_string("email_templates/internal/inactiverequest.txt", {'inactiverequest':inactiverequest}, plaintext_context)
	msg = EmailMultiAlternatives("VetCove Inactive Request", text_body, "The VetCove Team <info@vetcove.com>",[
	"mitch@vetcove","alex@vetcove.com"])
	msg.send()
	return

def composeContactForm(contact):
	plaintext_context = Context(autoescape=False) # HTML escaping not appropriate in plaintext
	text_body = render_to_string("email_templates/internal/contact.txt", {'contact':contact}, plaintext_context)
	msg = EmailMultiAlternatives("VetCove Contact Message", text_body, "The VetCove Team <info@vetcove.com>",[
	"mitch@vetcove","alex@vetcove.com"])
	msg.send()
	return

