from django.shortcuts import render_to_response, redirect
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
from django.utils.timezone import utc
import json, math, difflib, locale, time, re, string
from datetime import datetime
import balanced
from helper.model_imports import *
import payment.views as payment_view
import emails.views as email_view

###########################################
#### Logins and new users #################
###########################################

def loginview(request):
	next = request.GET.get('next',None)
	action = request.GET.get('action',None)
	if request.user.is_authenticated():
		return HttpResponseRedirect("/account/profile")
	return render_to_response('account/login.html',{'next':next,'action':action},context_instance=RequestContext(request))

def lgnrequest(request):
	username = request.POST['email']
	username = username.lower()
	password = request.POST['password']
	rememberme = request.POST.get('rememberme','')
	user = authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			if 'shoppingcart' in request.session:
				bu = BasicUser.objects.get(user=user)
				user_shoppingcart = ShoppingCart.objects.get(user=bu)
				session_shoppingcart = ShoppingCart.objects.get(id=request.session['shoppingcart'])
				for cartitems in session_shoppingcart.cartitem_set.all():
					if not CartItem.objects.filter(item=cartitems.item,shoppingcart=user_shoppingcart).exists():			
						ci = CartItem(item=cartitems.item,price=cartitems.item.price,shoppingcart=user_shoppingcart,quantity=1)
						ci.save()
			login(request,user)
			if rememberme:
				request.session.set_expiry(500000)
			else:
				request.session.set_expiry(0)
			try:
				request.GET['next']
				return HttpResponseRedirect(request.GET['next'])
			except:
				return HttpResponseRedirect("/account/profile")
		else:
			return render_to_response('account/login.html',{'outcome':'This account no longer exists'},context_instance=RequestContext(request))

	else:
		return render_to_response('account/login.html',{'outcome':'Your email and/or password was incorrect'},context_instance=RequestContext(request))

def checkemail(request):
	if request.method == "GET":
		email = request.GET['email']
		if User.objects.filter(username=email).count():
			return HttpResponse(json.dumps('invalid'), content_type='application/json')
		else:
			return HttpResponse(json.dumps('valid'), content_type='application/json')
	return HttpResponse(json.dumps('error'), content_type='application/json')
		
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def forgotpassword(request):
	return render_to_response('account/passwordreset.html',context_instance=RequestContext(request))

###########################################
#### Account Settings #####################
###########################################

@login_required
def notifications(request):
	notifications = request.user.basicuser.notification_set.all()
	return render_to_response('account/notifications.html',{'notification_set':notifications},context_instance=RequestContext(request))	

@login_required
def clearNotifications(request):
	notifications = Notification.objects.filter(user=request.user.basicuser)
	for notification in notifications:
		if not notification.viewed:
			notification.viewed = True
			notification.save()
	return HttpResponseRedirect('/account/notifications')

@login_required
def updateNotification(request):
	if request.method == "POST":
		notification = Notification.objects.get(id=request.POST.get('notification_id',''))
		if notification.user == request.user.basicuser:
			notification.viewed = True
			notification.save()
			if hasattr(notification,'sellermessagenotification'):
				return HttpResponseRedirect('/account/messages/'+str(notification.sellermessagenotification.sellermessage.item.id))
			elif hasattr(notification,'sellerquestionnotification'):
				return HttpResponseRedirect('/account/sellerquestions')
			elif hasattr(notification,'buyerquestionnotification'):
				return HttpResponseRedirect('/account/buyerquestions')
			elif hasattr(notification,'soldnotification'):
				return HttpResponseRedirect('/account/sellhistory')
			elif hasattr(notification,'authorizedbuyernotification'):
				return HttpResponseRedirect('/item/'+str(notification.authorizedbuyernotification.item.id)+'/details')
			elif hasattr(notification,'soldpaymentnotification'):
				return HttpResponseRedirect('/account/sellhistory')
			elif hasattr(notification,'shippednotification'):
				return HttpResponseRedirect('/account/buyhistory')
			elif hasattr(notification,'payoutnotification'):
				if notification.payoutnotification.success:
					return HttpResponseRedirect('/account/payouthistory')
				else:
					return HttpResponseRedirect('/account/payment')	
	return HttpResponseRedirect('/account/notifications')

@login_required
def updateGeneralSettings(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = request.user.basicuser
		bu.firstname = request.POST.get('firstname','')
		bu.lastname = request.POST.get('lastname','')
		bu.email = request.POST.get('email','')
		zipcode = request.POST.get('zipcode','')
		if bu.zipcode != int(zipcode):
			bu.zipcode = zipcode
			try:
				latlong_obj = LatLong.objects.get(zipcode=int(zipcode))
				bu.city = latlong_obj.city
				bu.county = latlong_obj.county
				bu.state = latlong_obj.state
			except:
				latlong_obj = None
		bu.save()
		return HttpResponseRedirect('/account/profile?s=info')
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def updateSellerSettings(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = request.user.basicuser
		bu.company = request.POST.get('company','')
		bu.businesstype = request.POST.get('business','')
		bu.website = request.POST.get('website','')
		phonenumber = request.POST.get('phonenumber','')
		phonenumber = re.sub("[^0-9]", "", phonenumber)
		try:
			phonenumber = int(phonenumber)
			bu.phonenumber = phonenumber
		except:
			phonenumber = None
		bu.save()
		return HttpResponseRedirect('/account/profile?s=info')
	else:
		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def updatePassword(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = request.user.basicuser
		op = request.POST.get('oldpassword','')
		np = request.POST.get('newpassword','')
		if bu.user.check_password(op):
			bu.user.set_password(np)
			bu.user.save()
		else:
			return HttpResponseRedirect('/account/profile?e=password')
		return HttpResponseRedirect('/account/profile?s=password')
	else:
		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def updatesettingsnewsletter(request):
	if request.user.is_authenticated() and request.method=="POST":
		if request.POST.get('newsletter',''):
			request.user.basicuser.newsletter = True
		else:
			request.user.basicuser.newsletter = False
		request.user.basicuser.save()
		return HttpResponseRedirect('/account/usersettings')
	else:
		return render_to_response('general/index.html',context_instance=RequestContext(request)) 

@login_required
def deleteAccount(request):
	if request.user.is_authenticated() and request.method=="POST":
		request.user.is_active = False
		request.user.save()
		logout(request)
		for item in request.user.basicuser.item_set.all():
			item.liststatus = 'disabled'
			item.save()
		return HttpResponseRedirect('/')

@login_required
def wishlist(request):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		saveditems = bu.saveditem_set.all()
		items = []
        	for si in saveditems:
        		items.append(si.item)
		return render_to_response('account/buying/wishlist.html',{"wishlist":True,"items":items},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))
   
@login_required
def contactMessages(request):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		contactmessages = SellerMessage.objects.filter(buyer=bu)
		return render_to_response('account/buying/contactmessages.html',{"contactmessages":True,"contactmessages":contactmessages},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))
   		
@login_required
def listings(request,listingtype):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		if listingtype == 'all':
			listeditems = bu.item_set.all()
		elif listingtype =='inactive':
			listeditems = bu.item_set.all().filter(liststatus__in=['sold','unsold'])
		else:
			listeditems = bu.item_set.all().filter(liststatus=listingtype)
		return render_to_response('account/selling/listeditems.html',{"listpage":True,"items":listeditems, "listingtype":listingtype},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))
 
@login_required
def buyhistory(request):
	if request.user.is_authenticated():
		return render_to_response('account/buying/buyhistory.html',{'buyhistory':True},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def payoutHistory(request):
	dict = {}
	payout_set = request.user.basicuser.payout_set.all()
	dict['total_payout'] = sum([payout.amount for payout in payout_set])
	total_items = [payout.purchaseditem_set.all() for payout in payout_set]
	total_item_count = 0
	for order in total_items:
		for pi in order:
			total_item_count += pi.quantity
	dict['total_items'] = total_item_count
	if total_item_count > 0:
		dict['total_items_average'] = int(dict['total_payout']/total_item_count)
	else:
		dict['total_items_average'] = 0
   	return render_to_response('account/selling/payouthistory.html',dict,context_instance=RequestContext(request))

@login_required
def sellhistory(request):
	if request.user.is_authenticated():
		return render_to_response('account/selling/sellhistory.html',{'sellhistory':True},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def usersettings(request):
	if request.user.is_authenticated():
		return render_to_response('account/settings.html',{},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def profile(request):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		dict = {'basicuser':bu,'profile':True}
		if request.method == "GET":
			if request.GET.get('e',''):
				dict['error']= request.GET.get('e','')
			if request.GET.get('s',''):
				dict['success']= request.GET.get('s','')
		return render_to_response('account/profile.html',dict,context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def payment(request):
	return render_to_response('account/payment.html',{'payment':True,'BALANCED_MARKETPLACE_ID':settings.BALANCED_MARKETPLACE_ID},context_instance=RequestContext(request))

#################################################
### Updating Payment Information  ###############
#################################################

#Calls the addBalancedBankAccount method
@login_required
def addBankAccount(request):
	if request.method == "POST":
		addBA = payment_view.addBalancedBankAccount(request)
		return HttpResponse(json.dumps({'status':addBA['status'],'error':addBA['error']}), content_type='application/json')
	return HttpResponse(json.dumps({'status':500,'error': 'Not a POST method'}), content_type='application/json')

#Calls the addBalancedCard method
@login_required
def addCreditCard(request):
	if request.method == "POST":
		addCC = payment_view.addBalancedCard(request)
		return HttpResponse(json.dumps({'status':addCC['status'],'error':addCC['error']}), content_type='application/json')
	return HttpResponse(json.dumps({'status':500,'error': 'Not a POST method'}), content_type='application/json')
	
@login_required
def account_deletecreditcard(request,creditcardid):
	if request.method=="POST":
		bc = BalancedCard.objects.get(id=creditcardid)
		payment_view.deleteBalancedCard(request,bc)
	return HttpResponseRedirect('/account/payment')
	
###########################################
#### Updating Listings ####################
###########################################
@login_required
def editListingInactive(request,itemid):
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and item.user == request.user.basicuser:
		item.liststatus = 'unsold'
		inactive_model = InactiveRequest(item=item,reason=request.POST['inactive-reason'])
		inactive_model.save()
		item.save()
		email_view.composeInactiveRequest(inactive_model)
	return HttpResponseRedirect(request.POST['page'])

@login_required
def editListingActive(request,itemid):
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and item.user == request.user.basicuser:
		if item.quantity > 0:
			item.liststatus = 'active'
			item.save()
	return HttpResponseRedirect(request.POST['page'])

@login_required
def editListingRelist(request,itemid):
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and item.user == request.user.basicuser:
		quantity = request.POST['quantity']
		if quantity > 0:
			item.quantity = quantity
			item.liststatus = 'active'
			item.save()
			return HttpResponseRedirect('/item/'+str(item.id)+'/details')
	return HttpResponseRedirect(request.POST['page'])

###########################################
#### Saving and Removing - Wishlist #######
###########################################
def saveitem(request):
	item = Item.objects.get(id=request.POST['id'])
	if request.method == "POST" and request.user.is_authenticated():
		if (request.POST['action'] == "save"):
			if not SavedItem.objects.filter(user = BasicUser.objects.get(user=request.user),item=item).exists():
				si = SavedItem(user = BasicUser.objects.get(user=request.user),item=item)
				item.savedcount += 1
				si.save()
		else:
			if SavedItem.objects.filter(user = BasicUser.objects.get(user=request.user),item=item).exists():
				si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
				si.delete()
				item.savedcount -= 1
		return HttpResponse(json.dumps({'status':"100"}), content_type='application/json')
	else:
		redirectURL = str('/login?next=/item/'+str(item.id)+"/details&action=save")
		return HttpResponse(json.dumps({'status':"400",'redirect':redirectURL}), content_type='application/json')

@login_required
def removeitem(request):
	if request.method == "POST" and request.user.is_authenticated():
		item = Item.objects.get(id=int(request.POST['itemid']))
		si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
		si.delete()
		return HttpResponseRedirect("/account/wishlist")
	return render_to_response('general/index.html',context_instance=RequestContext(request))






