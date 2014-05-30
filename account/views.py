from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.timezone import utc
import json, math, difflib, locale, time, re, string, balanced
from datetime import datetime
from account.forms import *
from helper.model_imports import *

###########################################
#### Basic Pages ##########################
###########################################
def dashboard(request):
	categories = ['Biologicals','Dental Care','Diagnostics','Eye and Ear','Fluid and Drugs','Nutrition','Pharmaceutical','Surgery','Wound Care','X-Ray']
	products_one,products_two,products_three,products_four = None,None,None,None
	product_rows = {'Recently Viewed Items You May Be Interested In':products_one,
			'New VetCove Marketplace Items':products_one,
			'Promotional Products You May Be Interested In':products_two,
			'Newly Added Products You May Be Interested In':products_three,
			'Top Products Trending on VetCove':products_four
				}
	return render_to_response('account/pages/browse/dashboard.html',{'dashboard':True,'product_rows':product_rows,'categories':categories},context_instance=RequestContext(request))
def new(request):
	return render_to_response('account/pages/browse/new.html',{'browse_new':True},context_instance=RequestContext(request))
def recent(request):
	return render_to_response('account/pages/browse/recent.html',{'browse_recent':True},context_instance=RequestContext(request))
def trending(request):
	return render_to_response('account/pages/browse/trending.html',{'browse_trending':True},context_instance=RequestContext(request))
def deals(request):
	return render_to_response('account/pages/browse/deals.html',{'browse_deals':True},context_instance=RequestContext(request))

###########################################
#### Portal Pages #########################
###########################################
def product(request,productname):
	product = Product.objects.get(name=productname)
	return render_to_response('product/product2.html',{'product':product},context_instance=RequestContext(request))
def company(request,companyname):
	return render_to_response('search/company.html',{},context_instance=RequestContext(request))

### Credits ###
@login_required
def creditsMissions(request):
	today = datetime.now()
	month = today.strftime('%B')
	return render_to_response('account/pages/credits/creditsmissions.html',{'account_credits_missions':True,'month':month},context_instance=RequestContext(request))

@login_required
def creditsStore(request):
	return render_to_response('account/pages/credits/creditsstore.html',{'account_credits_store':True},context_instance=RequestContext(request))

@login_required
def creditsHistory(request):
	return render_to_response('account/pages/credits/creditshistory.html',{'account_credits_history':True},context_instance=RequestContext(request))

### Orders ###
@login_required
def orders(request):
	return render_to_response('account/pages/orders.html',{'account_orders':True},context_instance=RequestContext(request))

### Returns ###
@login_required
def returns(request):
	return render_to_response('account/pages/returns.html',{'account_returns':True},context_instance=RequestContext(request))

### Analytics ###
@login_required
def analytics(request):
	return render_to_response('account/pages/analytics.html',{'account_analytics':True},context_instance=RequestContext(request))

### Questions ###
@login_required
def answeredQuestions(request):
	return render_to_response('account/pages/questions/questions.html',{'account_questions':True},context_instance=RequestContext(request))

@login_required
def askedQuestions(request):
	return render_to_response('account/pages/questions/questions.html',{'account_questions':True},context_instance=RequestContext(request))

@login_required
def answerQuestion(request,questionid):
	return render_to_response('account/pages/questions/writequestion.html',{'account_questions':True},context_instance=RequestContext(request))

@login_required
def askQuestion(request,productid):
	return render_to_response('account/pages/questions/writequestion.html',{'account_questions':True},context_instance=RequestContext(request))

### Reviews ###
@login_required
def reviewsReviews(request):
	return render_to_response('account/pages/reviews/reviews.html',{'account_reviews':True},context_instance=RequestContext(request))

@login_required
def reviewsHistory(request):
	return render_to_response('account/pages/reviews/reviewshistory.html',{'account_reviews':True},context_instance=RequestContext(request))

@login_required
def reviewsWriteReview(request,reviewid):
	if request.method=="GET":
		next = request.GET.get('next',False)
	return render_to_response('account/pages/reviews/writereview.html',{'account_reviews':True,'next':next},context_instance=RequestContext(request))

### Referrals ###
@login_required
def referrals(request):
	return render_to_response('account/pages/referrals.html',{'account_referrals':True},context_instance=RequestContext(request))

### Sell ###
@login_required
def sell(request):
	return render_to_response('account/pages/sell.html',{'account_sell':True},context_instance=RequestContext(request))

### Payments ###
@login_required
def payments(request):
	return render_to_response('account/pages/payments.html',{'account_payments':True},context_instance=RequestContext(request))

### Settings ###
@login_required
def settings(request):
	return render_to_response('account/pages/settings.html',{'account_settings':True},context_instance=RequestContext(request))

### Profile ###
@login_required
def profile(request):
	return render_to_response('account/pages/profile.html',{'account_profile':True},context_instance=RequestContext(request))



###########################################
#### Cart and Wishlist ####################
###########################################


### Cart ###
def cart(request):
	return render_to_response('account/pages/cart.html',context_instance=RequestContext(request))

### Wishlist ###
@login_required
def wishlist(request):
	return render_to_response('account/pages/wishlist.html',context_instance=RequestContext(request))


###########################################
#### Login and Sign Up ####################
###########################################
def signin(request):
	next = request.GET.get('next',None)
	action = request.GET.get('action',None)
	if request.user.is_authenticated():
		return HttpResponseRedirect("/account/profile")
	return render_to_response('account/sign/signin.html',{'next':next,'action':action,'login':True},context_instance=RequestContext(request))

def signup(request):
	next = request.GET.get('next',None)
	action = request.GET.get('action',None)
	if request.user.is_authenticated():
		return HttpResponseRedirect("/account/profile")
	return render_to_response('account/sign/signup.html',{'next':next,'action':action},context_instance=RequestContext(request))

#@login_required
def newAccountBasic(request):
	gpos = GPO.objects.all()
	return render_to_response('account/sign/newaccount_base.html',{'gpos':gpos},context_instance=RequestContext(request))

def loginform(request):
	action = request.POST.get('action','')
	rememberme = request.POST.get('rememberme','')
	username = request.POST['username']
	username = username.lower()
	password = request.POST['password']
	next = request.POST['next']
	user = authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			if rememberme:
				request.session.set_expiry(500000)
			else:
				request.session.set_expiry(0)
			if next:
				return HttpResponseRedirect(next)
			else:
				return HttpResponseRedirect("/")
		else:
			return render_to_response('account/sign/signin.html',{'login':True,'login_outcome':'This account no longer exists'},context_instance=RequestContext(request))
	else:
		return render_to_response('account/sign/signin.html',{'login':True,'login_outcome':'Your email and/or password was incorrect'},context_instance=RequestContext(request))
	return HttpResponseRedirect("/")

def signupform(request):
	action = request.POST.get('action','')
	rememberme = request.POST.get('rememberme','')
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	username = request.POST.get('username')
	password = request.POST['password']
	confirmpassword = request.POST['confirmpassword']
	if password != confirmpassword:
		return render_to_response('account/sign/signin.html',{'signup':True,'signup_outcome':'Passwords do not match'},context_instance=RequestContext(request))
	user = User.objects.create_user(username,username,password)
	user.save()
	basicuser = BasicUser(user=user)
	basicuser.save()
	user = authenticate(username=user,password=password)
	login(request,user)
	return HttpResponseRedirect("/newaccount/basic")

@login_required
def newaccountform(request):
	bu = request.user.basicuser
	practitioner_name = request.POST.get('practitioner_name','')
	clinic_name = request.POST.get('clinic_name','')
	website = request.POST.get('url','')
	address_one = request.POST.get('address_one','')
	address_two = request.POST.get('address_two','')
	city = request.POST.get('city','')
	state = request.POST.get('state','')
	zipcode = request.POST.get('zipcode','')
	phonenumber = request.POST.get('phonenumber','')
	organization = request.POST.get('organization','')
	large_animal = request.POST.get('large_animal','')
	small_animal = request.POST.get('small_animal','')
	equine =  request.POST.get('equine','')
	address = Address(name=clinic_name,
						address_one=address_one,
						address_two=address_two,
						city=city,
						state=state,
						zipcode=zipcode)
	address.save()
	clinic_object = Clinic(clinic_name=clinic_name,
						website=website,
						email=request.user.username,
						address=address,
						phonenumber=phonenumber,
						organization_type=organization,
						large_animal=large_animal,
						small_animal=small_animal,
						equine=equine)
	clinic_object.save()
	bu.clinic = clinic_object
	bu.save()
	gpos = GPO.objects.all()
	for gpo in gpos:
		gpo_name = request.POST.get("gpo_"+gpo.name,'') # Is this GPO selected?
		if gpo_name:
			gpo.clinics.add(clinic_object)
			gpo.save()
	#Create a shopping cart for this clinic
	shoppingcart = ShoppingCart(clinic=clinic_object,)
	return HttpResponseRedirect("/account/profile")

###########################################
#### Logins and new users #################
###########################################

def signupview(request):
	next = request.GET.get('next',None)
	action = request.GET.get('action',None)
	if request.user.is_authenticated():
		return HttpResponseRedirect("/account/profile")
	return render_to_response('account/signin.html',{'next':next,'action':action,'signup':True},context_instance=RequestContext(request))

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

def checkpromo(request):
	if request.method == "GET":
		promo = request.GET.get('promo','')
		try:
			promocode = PromoCode.objects.get(code=promo)
			return HttpResponse(json.dumps({'status':201,'text':promocode.promo_text}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'status':500}), content_type='application/json')
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
		bu.zipcode = request.POST.get('zipcode','')
		bu.city = request.POST.get('city','')
		bu.state = request.POST.get('state','')
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
		mainimage = request.FILES.get("mainimage",'')
		try:
			phonenumber = int(phonenumber)
			bu.phonenumber = phonenumber
		except:
			phonenumber = None
		if mainimage:
			bu.mainimage = mainimage
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
		for item in request.user.basicuser.item_set.all():
			item.liststatus = 'disabled'
			item.save()
		request.user.is_active = False
		request.user.save()
		logout(request)
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
def bonus(request):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		feedback = True if bu.feedback_set.exists() else False
		return render_to_response('account/bonus/bonus.html',{"bonus":True,'feedback':feedback},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))
 
@login_required
def referral(request):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		return render_to_response('account/bonus/referral.html',{"bonus":True},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))

@login_required
def feedback(request):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		return render_to_response('account/bonus/feedback.html',{"bonus":True},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))
  
@login_required
def feedbackForm(request):
	if request.method == 'POST':
		form = FeedbackForm(request.POST)
		if form.is_valid():		
			love = form.cleaned_data['love']
			change = form.cleaned_data['change']
			feedback = Feedback(user=request.user.basicuser,love=love,change=change)
			feedback.save()
			updateCredits(request.user.basicuser)
		return HttpResponseRedirect('/account/feedbackthanks')
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))

@login_required
def feedbackThanks(request):
	return render_to_response('account/bonus/feedback.html',{"bonus":True,"success":True},context_instance=RequestContext(request))

@login_required
def referralForm(request):
	if request.method == 'POST':
		form = ReferralForm(request.POST)
		if form.is_valid():		
			emails = form.cleaned_data['emails']
			emails = str(emails.replace("[","",).replace("]","",).replace(" ","",).replace("'","",))
			emails = emails.split(",")
			email_view.composeReferral(request.user.basicuser,emails)
			return HttpResponseRedirect('/account/referralthanks')
		else:
			return HttpResponseRedirect('/account/referral')
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))

@login_required
def referralThanks(request):
	return render_to_response('account/bonus/referral.html',{"bonus":True,"success":True},context_instance=RequestContext(request))
	
@login_required
def bonusHistory(request):
	if request.user.is_authenticated():
		bu = request.user.basicuser
		credits = updateCredits(bu)
		return render_to_response('account/bonus/bonushistory.html',{"bonus":True,'credits':credits},context_instance=RequestContext(request))
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
	basicuser = request.user.basicuser
	providers = BasicUser.objects.all()
	unapproved_vendors = basicuser.unapprovedvendoruser.all()
	unapproved_vendors = [uv.vendor for uv in unapproved_vendors]
	if request.user.is_authenticated():
		return render_to_response('account/settings.html',{'providers':providers,'unapprovedvendors':unapproved_vendors},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def updateProviders(request):
	if request.method == 'POST' and request.user.is_authenticated():
		provider_id = request.POST.get('provider-id','')
		provider_value = request.POST.get('provider-value','')
		vendor = BasicUser.objects.get(id=provider_id)
		if provider_value == 'true':
			if UnapprovedVendor.objects.filter(user=request.user.basicuser,vendor=vendor).exists():
				provider = UnapprovedVendor.objects.get(user=request.user.basicuser,vendor=vendor)
				provider.delete()
		else:
			obj, created = UnapprovedVendor.objects.get_or_create(user=request.user.basicuser,vendor=vendor)
			obj.save()
		return HttpResponse(json.dumps({'status':201}), content_type='application/json')
	return HttpResponse(json.dumps({'status':500}), content_type='application/json')


# @login_required
# def profile(request):
# 	if request.user.is_authenticated():
# 		bu = request.user.basicuser
# 		dict = {'basicuser':bu,'profile':True}
# 		if request.method == "GET":
# 			if request.GET.get('e',''):
# 				dict['error']= request.GET.get('e','')
# 			if request.GET.get('s',''):
# 				dict['success']= request.GET.get('s','')
# 		return render_to_response('account/profile.html',dict,context_instance=RequestContext(request))
# 	else:
#    		return render_to_response('general/index.html',context_instance=RequestContext(request))

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
			if not SavedItem.objects.filter(user = request.user.basicuser,item=item).exists():
				si = SavedItem(user = request.user.basicuser,item=item)
				item.savedcount += 1
				si.save()
		else:
			if SavedItem.objects.filter(user = request.user.basicuser,item=item).exists():
				si = SavedItem.objects.get(user = request.user.basicuser,item=item)
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
		si = SavedItem.objects.get(user = request.user.basicuser,item=item)
		si.delete()
		return HttpResponseRedirect("/account/wishlist")
	return render_to_response('general/index.html',context_instance=RequestContext(request))






