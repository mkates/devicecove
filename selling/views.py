from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
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
from listing.models import *
import payment.views as payment_view
import emails.views as email_view
import helper.commission as commission
############################################
########## Selling Portal ##################
############################################
def portalHelp(request):
	return render_to_response('sellerportal/help.html',{'seller':True},context_instance=RequestContext(request))

def portalInventory(request):
	### !!! Add Security Layer Here ###
	inventories = Inventory.objects.all()
	return render_to_response('sellerportal/inventory.html',{'seller':True,'portal_inventory':True,'inventories':inventories},context_instance=RequestContext(request))

def portalProduct(request):
	### !!! Add Security Layer Here ###
	products = Product.objects.all()
	return render_to_response('sellerportal/product/home.html',{'seller':True,'portal_product':True,'products':products},context_instance=RequestContext(request))
 
def portalProductEdit(request,productid):
	### !!! Add Security Layer Here ###
	product = Product.objects.get(id=productid)
	return render_to_response('sellerportal/product/edit.html',{'seller':True,'portal_product':True,'portal_products_edit':True,'product':product},context_instance=RequestContext(request))

def portalProductAnalytics(request,productid):
	### !!! Add Security Layer Here ###
	product = Product.objects.get(id=productid)
	return render_to_response('sellerportal/product/analytics.html',{'seller':True,'portal_product':True,'portal_products_analytics':True,'product':product},context_instance=RequestContext(request))

def portalProductPromotions(request,productid):
	### !!! Add Security Layer Here ###
	product = Product.objects.get(id=productid)
	return render_to_response('sellerportal/product/promotions.html',{'seller':True,'portal_product':True,'portal_products_promotions':True,'product':product},context_instance=RequestContext(request))

def portalPurchases(request):
	return render_to_response('sellerportal/purchases.html',{'seller':True,'portal_purchases':True},context_instance=RequestContext(request))

def portalIndividualPurchase(request,purchaseid):
	return render_to_response('sellerportal/individualpurchase.html',{'seller':True,'portal_purchases':True},context_instance=RequestContext(request))

def portalCommunity(request):
	return render_to_response('sellerportal/community.html',{'seller':True,'portal_community':True},context_instance=RequestContext(request))

def portalPromotions(request):
	return render_to_response('sellerportal/promotions.html',{'seller':True,'portal_promotions':True},context_instance=RequestContext(request))

def portalAnalytics(request):
	return render_to_response('sellerportal/analytics.html',{'seller':True,'portal_analytics':True},context_instance=RequestContext(request))

def portalReports(request):
	return render_to_response('sellerportal/reports.html',{'seller':True,'portal_reports':True},context_instance=RequestContext(request))

def portalAccount(request):
	return render_to_response('sellerportal/account.html',{'seller':True,'portal_account':True},context_instance=RequestContext(request))


############################################
########## Selling #########################
############################################


### When a message is sent to the seller (offline item) ###
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
		notification = SellerMessageNotification(user=seller,sellermessage=sm)
		notification.save()
		email_view.composeEmailContactMessage_Seller(seller,sm)
		status = 201
	else:
		status = 500
	return HttpResponse(json.dumps(status), content_type='application/json')

### When a seller wants to view all of their buyer messages ###
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
			item.commission_paid = True
			item.save()
			return render_to_response('account/selling/messages.html',{'item':item},context_instance=RequestContext(request))
		else:
			payment_methods = False
			payments =  request.user.basicuser.payment_set.all()
			for payment in payments:
				if hasattr(payment,'balancedcard') or hasattr(payment,'balancedbankaccount'):
					payment_methods = True
			dict = {'gate':True,'paying':True,'payment_methods':payment_methods,'item':item,'standard_commission':standard_commission,'net_commission':net_commission,'discount':savings,'commission_percent':commission.commissionPercentage(item.price)}
			if request.GET.get('e',''):
				dict['error'] = request.GET.get('e')
			return render_to_response('account/contact_gate.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/')

#################################################
### Contact Message Follow Up From Emaik ########
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
	
	
#################################################
### Gateway for viewing buyer interest  #########
#################################################
# Calls the balanced create card, which adds the card to the user and sets default credit card
@login_required
def newcard_chargecommission(request,itemid):
	item = Item.objects.get(id=itemid)
	# If commission already paid, skip to messages
	if item.commission_paid == True:
		return HttpResponse(json.dumps({'status':201}), content_type='application/json')
	if request.user.basicuser == item.user and request.method == 'POST':
		balanced_addCard = payment_view.addBalancedCard(request)
		# If adding the card fails, serve an error message
		if balanced_addCard['status'] != 201:
			return HttpResponse(json.dumps({'status':balanced_addCard['status'],'error':balanced_addCard['error']}), content_type='application/json')	
		try:
			card = balanced_addCard['card']
			bu = request.user.basicuser
			card_uri = card.uri
			balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
			customer = balanced.Customer.find(balanced_addCard['balanceduri'])
			amount = commission.commission(item)
			description = "Charge for item "+str(item.id)
			debit = customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=card_uri,description=description)
			if not debit.status == "succeeded":
				return HttpResponse(json.dumps({'status':501,'error':'Failed to charge your card.'}), content_type='application/json')
			item.commission_paid = True
			item.save()
			commission_obj = Commission(item=item,price=item.price,amount=amount,payment=card,transaction_number=debit.transaction_number)
			commission_obj.save()
			email_view.composeEmailCommissionCharged(bu,commission_obj)
			return HttpResponse(json.dumps({'status':201}), content_type='application/json')
		except Exception,e:
			print e
			return HttpResponse(json.dumps({'status':501,'error':'Failed to charge your card.'}), content_type='application/json')
	return HttpResponse(json.dumps({'status':501,'error':'Error passing security credentials'}), content_type='application/json')

# Using an existing card to pay the commission fees
@login_required
def gatePayment(request,paymentid,itemid):
	item = Item.objects.get(id=itemid)
	if item.commission_paid == True:
		return HttpResponseRedirect('/account/messages/'+str(item.id))
	if request.user.basicuser == item.user and request.method == 'POST':
		try:
			payment = Payment.objects.get(id=paymentid)
			if payment.user == request.user.basicuser:
				bu = request.user.basicuser
				balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
				customer = balanced.Customer.find(bu.balanceduri)
				amount = commission.commission(item)
				uri = payment.balancedcard.uri if hasattr(payment,'balancedcard') else payment.balancedbankaccount.uri
				debit = customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=uri)
				if not debit.status == "succeeded":
					return HttpResponseRedirect('/account/messages/'+str(item.id)+"?e=fail")
				item.commission_paid = True
				item.save()
				commission_obj = Commission(item=item,price=item.price,amount=amount,payment=payment,transaction_number=debit.transaction_number)
				commission_obj.save()
				email_view.composeEmailCommissionCharged(bu,commission_obj)
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
		email_view.composeEmailItemShipped_Buyer(request.user.basicuser,pi)
		notification = ShippedNotification(user=pi.buyer,purchaseditem=pi)
		notification.save()
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
		notification = AuthorizedBuyerNotification(user=buyer,item=item)
		notification.save()
		if created:
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
		email_view.composeFileReport(report)
	return HttpResponseRedirect("/account/reportproblem/"+str(purchaseditemid))
	
		





################ Currently Unused Functions ##################


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
			debit = customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=bank_uri)
			if not debit.status == "succeeded":
				return HttpResponse(json.dumps({'status':501,'error':'Failed to charge your bank account.'}), content_type='application/json')
			item.commission_paid = True
			item.save()
			commission_obj = Commission(item=item,price=item.price,amount=amount,payment=bank,transcation_number=debit.transaction_number)
			commission_obj.save()
			email_view.composeEmailCommissionCharged(request,bu,commission_obj)
			return HttpResponse(json.dumps({'status':201}), content_type='application/json')
		except Exception,e:	
			print e
			return HttpResponse(json.dumps({'status':501,'error':'Failed to charge your bank account.'}), content_type='application/json')
	return HttpResponse(json.dumps({'status':501,'error':'Error passing security credentials'}), content_type='application/json')


















