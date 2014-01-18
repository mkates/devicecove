from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
import views_payment as payment_view
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import medapp.settings as settings
import json
import balanced

COMMISSION_PERCENTAGE = .09

@login_required
def messageseller(request,itemid):
	if request.user.is_authenticated() and request.method=="POST":
		item = Item.objects.get(id=itemid)
		bu = request.user.basicuser
		name = request.POST.get('contact-name','')
		email = request.POST.get('contact-email','')
		phone = request.POST.get('contact-phone','')
		reason = request.POST.get('contact-reason','')
		message = request.POST.get('contact-message','')
		seller = item.user
		sm = SellerMessage(buyer=bu,name=name,item=item,email=email,phone=phone,reason=reason,message=message) 
		sm.save()
		############################
		#### Send Email Here As Well
		############################
		status = 201
	else:
		status = 500
	return HttpResponse(json.dumps(status), content_type='application/json')

@login_required
def buyermessages(request,itemid):
	item = Item.objects.get(id=itemid)
	commission = int(item.price * COMMISSION_PERCENTAGE)
	# If the user logged in owns the item
	messages = item.sellermessage_set.all()
	if request.user.basicuser == item.user:
		if item.commission_paid:
			return render_to_response('account/selling/messages.html',{'item':item},context_instance=RequestContext(request))
		else:
			dict = {'gate':True,'item':item,'commission':commission}
			if request.GET.get('e',''):
				dict['error'] = request.GET.get('e')
			return render_to_response('account/contact_gate.html',dict,context_instance=RequestContext(request))

#################################################
### Gateway for viewing buyer interest  #########
#################################################

# Calls the balanced create card, which adds the card to the user and sets default credit card
@login_required
def newcard_chargecommission(request,itemid):
	item = Item.objects.get(id=itemid)
	if item.commission_paid == True:
		return HttpResponse(json.dumps({'status':201}), content_type='application/json')
	if request.user.basicuser == item.user and request.method == 'POST':
		balanced_addCard = payment_view.addBalancedCard(request)
		if balanced_addCard['status'] != 201:
			return HttpResponse(json.dumps({'status':balanced_addCard['status'],'error':balanced_addCard['error']}), content_type='application/json')	
		try:
			card = balanced_addCard['card']
			bu = request.user.basicuser
			card_uri = card.uri
			balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
			customer = balanced.Customer.find(bu.balanceduri)
			amount = int(item.price * COMMISSION_PERCENTAGE)*100
			customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=card_uri)
			item.commission_paid = True
			item.save()
			return HttpResponse(json.dumps({'status':201}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'status':501,'error':'Failed to charge your card.'}), content_type='application/json')
	return HttpResponse(json.dumps({'status':501,'error':'Error passing security credentials'}), content_type='application/json')

# New bank account, which adds the BA to the user and sets default credit card
@login_required
def newbank_chargecommission(request,itemid):
	item = Item.objects.get(id=itemid)
	if item.commission_paid == True:
		return HttpResponse(json.dumps({'status':201}), content_type='application/json')
	if request.user.basicuser == item.user and request.method == 'POST':
		balanced_addBankAccount = payment_view.addBalancedBankAccount(request)
		if balanced_addBankAccount['status'] != 201:
			return HttpResponse(json.dumps({'status':balanced_addBankAccount['status'],'error':balanced_addBankAccount['error']}), content_type='application/json')	
		try:
			bank = balanced_addBankAccount['bank']
			bu = request.user.basicuser
			bank_uri = bank.uri
			balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
			customer = balanced.Customer.find(bu.balanceduri)
			amount = int(item.price * COMMISSION_PERCENTAGE)*100
			customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=bank_uri)
			item.commission_paid = True
			item.save()
			return HttpResponse(json.dumps({'status':201}), content_type='application/json')
		except Exception,e:
			return HttpResponse(json.dumps({'status':501,'error':'Failed to charge your bank account.'}), content_type='application/json')
	return HttpResponse(json.dumps({'status':501,'error':'Error passing security credentials'}), content_type='application/json')

@login_required
def gatePayment(request,paymenttype,paymentid,itemid):
	item = Item.objects.get(id=itemid)
	if item.commission_paid == True:
		return HttpResponseRedirect('/account/messages/'+str(item.id))
	if request.user.basicuser == item.user and request.method == 'POST':
		try:
			if paymenttype == 'card':
				payment = BalancedCard.objects.get(id=paymentid)
			elif paymenttype == 'bank':
				payment = BalancedBankAccount.objects.get(id=paymentid)
			if payment.user == request.user.basicuser:
				bu = request.user.basicuser
				balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
				customer = balanced.Customer.find(bu.balanceduri)
				amount = int(item.price * COMMISSION_PERCENTAGE)*100
				customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=payment.uri)
				item.commission_paid = True
				item.save()
				return HttpResponseRedirect('/account/messages/'+str(item.id))
		except Exception,e:
			return HttpResponseRedirect('/account/messages/'+str(item.id)+"?e=fail")
	return HttpResponseRedirect('/account/messages/'+str(item.id)+"?e=fail")

	
#################################################
### Post Purchase Messaging  ####################
#################################################
@login_required
def purchasesellermessage(request,purchaseditemid):
	pi = PurchasedItem.objects.get(id=purchaseditemid)
	message = request.POST['buyer-message']
	pi.buyer_message = message
	pi.save()
	######################################
	#### Send Email To Buyer Here as Well
	#####################################
	return HttpResponseRedirect('/account/buyhistory')

@login_required
def purchaseshippinginfo(request,purchaseditemid):
	pi = PurchasedItem.objects.get(id=purchaseditemid)
	shipping_details = request.POST['shipping-details']
	shipped = request.POST.get('shipped','')
	if request.POST['submit'] == 'shipped':
		pi.item_sent = True
	else:
		pi.item_sent = False
	pi.seller_message = shipping_details
	pi.save()
	######################################
	#### Send Email To Buyer Here as Well
	#####################################
	return HttpResponseRedirect('/account/sellhistory')
	
@login_required
def authorizeBuyer(request,buyerid,itemid):
	item = Item.objects.get(id=itemid)
	if request.user.basicuser == item.user and request.method == 'POST':
		buyer = BasicUser.objects.get(id=buyerid)
		au = BuyAuthorization(seller=request.user.basicuser,buyer=buyer,item=item)
		obj, created = BuyAuthorization.objects.get_or_create(seller=request.user.basicuser,buyer=buyer,item=item)
		obj.save()
	return HttpResponseRedirect('/account/messages/'+str(item.id))

@login_required
def deauthorizeBuyer(request,buyerid,itemid):
	item = Item.objects.get(id=itemid)
	if request.user.basicuser == item.user and request.method == 'POST':
		buyer = BasicUser.objects.get(id=buyerid)
		try:
			ba = BuyAuthorization.objects.get(seller=request.user.basicuser,buyer=buyer,item=item)
			ba.delete()
			return HttpResponseRedirect('/account/messages/'+str(item.id))
		except Exception,e:
			print e
			return HttpResponseRedirect('/account/messages/'+str(item.id))
#################################################
### Sale Problems  ##############################
#################################################
@login_required
def reportproblem(request,purchaseditemid):
	pi = PurchasedItem.objects.get(id=purchaseditemid)
	return render_to_response('account/buying/report.html',{'pitem':pi},context_instance=RequestContext(request))

@login_required
def reportproblemform(request,purchaseditemid):
	pi = PurchasedItem.objects.get(id=purchaseditemid)
	if request.method == "POST":
		reason = request.POST.get('reason','')
		details = request.POST.get('details','')
		report = Report(purchased_item=pi,reason=reason,details=details)
		report.save()
	return HttpResponseRedirect("/account/reportproblem/"+str(purchaseditemid))