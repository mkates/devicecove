from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
import views_payment as payment_view
import views_email as email_view
import commission as commission
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

@login_required
def addPromoCode(request,itemid):
	dict = {}
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and item.user == request.user.basicuser: 
		promocode = request.POST.get('promocode','')
		promocode = promocode.lower()
		try:
			pc = PromoCode.objects.get(code=promocode.lower())
			if pc.active:
				item.promo_code = pc
				item.save()
				dict = {'status':201,'message':pc.promo_text}
			else:
				dict = {'status':400,'message':"You're too late! This code has expired! Sorry"}
		except:
			dict = {'status':500,'message':'This code does not exist'}
	else:
		dict = {'status':500,'message':'Not the owner of the item'}
	return HttpResponse(json.dumps(dict), content_type='application/json')

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
		email_view.composeEmailContactMessage_Seller(request,seller,sm)
		status = 201
	else:
		status = 500
	return HttpResponse(json.dumps(status), content_type='application/json')

@login_required
def buyermessages(request,itemid):
	item = Item.objects.get(id=itemid)
	net_commission = commission.commission(item)
	standard_commission = commission.originalCommission(item)
	savings = commission.commissionSavings(item)
	# If the user logged in owns the item
	messages = item.sellermessage_set.all()
	if request.user.basicuser == item.user:
		if item.commission_paid or net_commission == 0:
			#item.commission_paid = True
			#item.save()
			return render_to_response('account/selling/messages.html',{'item':item},context_instance=RequestContext(request))
		else:
			dict = {'gate':True,'item':item,'standard_commission':standard_commission,'net_commission':net_commission,'discount':savings,'commission_percent':commission.commissionPercentage(item.price)}
			if request.GET.get('e',''):
				dict['error'] = request.GET.get('e')
			return render_to_response('account/contact_gate.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/')
	
	
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
			customer = balanced.Customer.find(balanced_addCard['balanceduri'])
			amount = commission.commission(item)
			customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=card_uri)
			item.commission_paid = True
			item.save()
			commission_obj = Commission(item=item,price=item.price,amount=amount,payment_method='card',cc_payment=card)
			commission_obj.save()
			email_view.composeEmailCommissionCharged(request,bu,commission_obj)
			return HttpResponse(json.dumps({'status':201}), content_type='application/json')
		except Exception,e:
			print e
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
			customer = balanced.Customer.find(balanced_addBankAccount['balanceduri'])
			amount = commission.commission(item)
			customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=bank_uri)
			item.commission_paid = True
			item.save()
			commission_obj = Commission(item=item,price=item.price,amount=amount,payment_method='bank',ba_payment=bank)
			commission_obj.save()
			email_view.composeEmailCommissionCharged(request,bu,commission_obj)
			return HttpResponse(json.dumps({'status':201}), content_type='application/json')
		except Exception,e:	
			print e
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
				amount = commission.commission(item)
				customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=payment.uri)
				item.commission_paid = True
				item.save()
				if paymenttype == 'bank':
					commission_obj = Commission(item=item,price=item.price,amount=comm_amount,payment_method=paymenttype,ba_payment=payment)
				elif paymenttype == 'card':
					commission_obj = Commission(item=item,price=item.price,amount=comm_amount,payment_method=paymenttype,cc_payment=payment)
				commission_obj.save()
				email_view.composeEmailCommissionCharged(request,bu,commission_obj)
				return HttpResponseRedirect('/account/messages/'+str(item.id))
		except Exception,e:
			print e
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
	pi.seller_message = shipping_details
	if request.POST['submit'] == 'shipped' and pi.item_sent == False:
		pi.item_sent = True
		email_view.composeEmailItemShipped_Buyer(request,request.user.basicuser,pi)
		email_view.composeEmailItemShipped_Seller(request,request.user.basicuser,pi)
	else:
		pi.item_sent = False
	pi.save()
	return HttpResponseRedirect('/account/sellhistory')
	
@login_required
def authorizeBuyer(request,buyerid,itemid):
	item = Item.objects.get(id=itemid)
	if request.user.basicuser == item.user and request.method == 'POST':
		buyer = BasicUser.objects.get(id=buyerid)
		au = BuyAuthorization(seller=request.user.basicuser,buyer=buyer,item=item)
		obj, created = BuyAuthorization.objects.get_or_create(seller=request.user.basicuser,buyer=buyer,item=item)
		obj.save()
		if not created:
			email_view.composeEmailAuthorizedBuyer(item,buyer)
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
	
#################################################
### Contact Message Follow Up  ##################
#################################################
def updateListingState(request,action,token):
	dict = {}
	try:
		rt_obj = ReminderToken.objects.get(token=token)
		item = rt_obj.contact_message.item
	except:
		rt_obj = None
	if not rt_obj:
		dict = {'status':500,'error':'does_not_exist'}
	elif item.liststatus !='active':
		dict = {'status':500,'error':'not_active','item':item}
	elif action in ['sold','not_sold','different_sold']:
		rt_obj.action = action
		rt_obj.save()
		if action == 'not_sold':
			dict = {'status':201,'message':'not_sold','item':item}
		else:
			item.liststatus = 'sold'
			item.save()
			dict = {'status':201,'message':'sold','item':item}
	else:
		dict = {'status':500,'error':'does_not_exist'}
		
	return render_to_response('account/email_action_base.html',dict,context_instance=RequestContext(request))
	
		






















