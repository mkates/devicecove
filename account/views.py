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
import json, math, difflib, locale, time, re, string, balanced, random, us
from datetime import datetime
from account.forms import *
from helper.model_imports import *

###########################################
#### Basic Pages ##########################
###########################################
def dashboard(request):
	return render_to_response('account/pages/browse/dashboard.html',{'dashboard':True},context_instance=RequestContext(request))
def new(request):
	return render_to_response('account/pages/browse/new.html',{'browse_new':True},context_instance=RequestContext(request))
def recent(request):
	return render_to_response('account/pages/browse/recent.html',{'browse_recent':True},context_instance=RequestContext(request))
def trending(request):
	return render_to_response('account/pages/browse/trending.html',{'browse_trending':True},context_instance=RequestContext(request))
def deals(request):
	return render_to_response('account/pages/browse/deals.html',{'browse_deals':True},context_instance=RequestContext(request))
def rewardsRewards(request):
	return render_to_response('account/pages/browse/rewards/rewards.html',{'browse_rewards':True, 'browse_rewards_rewards':True},context_instance=RequestContext(request))
def rewardsStore(request):
	return render_to_response('account/pages/browse/rewards/store.html',{'browse_rewards':True, 'browse_rewards_store':True},context_instance=RequestContext(request))
def rewardsHistory(request):
	return render_to_response('account/pages/browse/rewards/history.html',{'browse_rewards':True, 'browse_rewards_history':True},context_instance=RequestContext(request))

###########################################
#### Portal Pages #########################
###########################################
def product(request,productname):
	product = Product.objects.get(name=productname)
	products = Product.objects.all()
	for pdt in products:
		pdt.details = getItemDetailsFromAProduct(pdt)
	return render_to_response('product/product2.html',{'product':product,'products':products},context_instance=RequestContext(request))

### Given a product, get details from all the item's listings ####
def getItemDetailsFromAProduct(product):
	items = product.item_set.all()
	lowprice,highprice = None, None
	msrp_lowprice,msrp_highprice = None,None
	suppliers = []
	quantity = 0
	for item in items:
		if not msrp_lowprice or item.msrp_price < msrp_lowprice:
			msrp_lowprice = item.msrp_price
		if not msrp_highprice or item.msrp_price > msrp_highprice:
			msrp_highprice = item.msrp_price 
		inventories = item.inventory_set.all()
		for inventory in inventories:
			if inventory.supplier not in suppliers:
				suppliers.append(inventory.supplier)
			quantity += inventory.quantity_available
			if not lowprice or inventory.base_price < lowprice:
				lowprice = inventory.base_price
			if not highprice or inventory.base_price > highprice:
				highprice = inventory.base_price
	return {'lowprice':lowprice,'highprice':highprice,'msrp_lowprice':msrp_lowprice,'msrp_highprice':msrp_highprice,'quantity':quantity,'suppliers':suppliers}

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
@login_required
def cart(request):
	return render_to_response('account/pages/cart.html',context_instance=RequestContext(request))

### Wishlist ###
@login_required
def wishlist(request):
	return render_to_response('account/pages/wishlist.html',context_instance=RequestContext(request))


###########################################
#### Login and Sign Up ####################
###########################################

# Sign in Page #
def signin(request):
	next = request.GET.get('next','')
	action = request.GET.get('action','')
	if request.user.is_authenticated():
		return HttpResponseRedirect("/dashboard")
	return render_to_response('account/sign/signin.html',{'next':next,'action':action,'login':True},context_instance=RequestContext(request))

# Sign up Page #
def signup(request):
	next = request.GET.get('next',None)
	action = request.GET.get('action',None)
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	return render_to_response('account/sign/signup.html',{'next':next,'action':action},context_instance=RequestContext(request))

# Log In Form #
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
			return render_to_response('account/sign/signin.html',{'login':True,'login_outcome':'This account is no longer active'},context_instance=RequestContext(request))
	else:
		return render_to_response('account/sign/signin.html',{'login':True,'login_outcome':'Your email and/or password were incorrect'},context_instance=RequestContext(request))
	return HttpResponseRedirect("/")

# Sign up Form #
def signupform(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			# 1. Get Cleaned Form Elements
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			confirmpassword = form.cleaned_data['confirmpassword']
			promocode = form.cleaned_data['promocode']
			usertype = form.cleaned_data['usertype']
			# 2. Check passwords match
			if password != confirmpassword: # Confirm passwords match
				return render_to_response('account/sign/signup.html',{'signup':True,'signup_outcome':'Passwords do not match','form':form},context_instance=RequestContext(request))
			# 3. Create the user object, make sure the username is unique
			try:
				user = User.objects.create_user(username,username,password)
				user.save()
			except:
				return render_to_response('account/sign/signup.html',{'signup':True,'signup_outcome':'Username already used'},context_instance=RequestContext(request))
			# 4. Create a Clinic Object or Create a Supplier Object
			basicuser = BasicUser(user=user)
			referrer_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
			if usertype == 'clinic':
				clinic = Clinic(email=username,referrer_id=referrer_id)
				clinic.save()
				basicuser.group = clinic
			else:
				supplier = Supplier(email=username,referrer_id=referrer_id)
				supplier.save()
				basicuser.group = supplier
			basicuser.save()
			# 6. Log User In 
			user = authenticate(username=user,password=password)
			login(request,user)
			if usertype=='clinic':
				return HttpResponseRedirect("/newaccount")
			else:
				return HttpResponseRedirect("/supplier/signup")
		else: # Form is not valid (should not happen because we check everything client side as well, but just in case)
			return render_to_response('account/sign/signup.html',{'signup':True,'signup_outcome':'Invalid Input'},context_instance=RequestContext(request))
	else: # If it is a GET request, send them back to /signup page
		return HttpResponseRedirect("/signup")

@login_required
def newSupplierSignup(request):
	supplier = request.user.basicuser.group_handle()
	if supplier.application_submitted == True:
		return render_to_response('account/sign/newaccount/supplier_complete.html',{'supplier':True},context_instance=RequestContext(request))
	else:
		states = [state.name for state in us.states.STATES] # Generates a list of all 50 states
		return render_to_response('account/sign/newaccount/supplier_signup.html',{'supplier':True,'states':states},context_instance=RequestContext(request))

@login_required
def supplierSignupForm(request):
	states = [state.name for state in us.states.STATES] # Generates a list of all 50 states
	supplier = request.user.basicuser.group_handle()
	if request.method == 'POST':
		form = SupplierSignupForm(request.POST)
		if form.is_valid():
			supplier.name = form.cleaned_data['name']
			supplier.primary_contact = form.cleaned_data['primary_contact']
			supplier.phonenumber = form.cleaned_data['phonenumber']
			address_one = form.cleaned_data['address_one']
			address_two = form.cleaned_data['address_two']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			address = Address(group = request.user.basicuser.group,
				name = supplier.name,
				address_one=address_one,
				address_two=address_two,
				city=city,
				state = state,
				zipcode = zipcode
				)
			supplier.website = form.cleaned_data['website']
			supplier.current_selling_method = form.cleaned_data['current_selling_method']
			supplier.interest_listings = form.cleaned_data['interest_listings']
			supplier.interest_community = form.cleaned_data['interest_community']
			supplier.interest_promotions = form.cleaned_data['interest_promotions']
			supplier.interest_direct = form.cleaned_data['interest_direct']
			supplier.application_submitted = True
			supplier.save()
	return HttpResponseRedirect('/supplier/signup')

# This method looks at a clinic's current field values to determine
# which parts of the sign up process are complete. It returns a dictionary with the completed steps
def clinicSignUpStatus(clinic):
	c = clinic
	signup_status = {'details':False,'address':False,'verification':False,'tos':False}
	if c.name and c.phonenumber and c.practice_type and c.organization_type and c.practice_type:
		signup_status['details'] = True
	if c.address:
		signup_status['address'] = True
	if c.license_no and c.practitioner_name:
		signup_status['verification'] = True
	if c.tos:
		signup_status['tos'] = True
	return signup_status

### The generic new account link, which automatically redirects to the last uncompleted step ###
@login_required
def newAccount(request):
	# Get the handle of the clinic and check the user is of type clinic
	group_handle = request.user.basicuser.group_handle()
	## If not a clinic, send them back to the homepage 
	if not hasattr(group_handle,'clinic'):
		return HttpResponseRedirect('/')
	signup_status = clinicSignUpStatus(group_handle)
	if not signup_status['details']:
		gpos = GPO.objects.all()
		return HttpResponseRedirect('/newaccount/details')
	if not signup_status['address']:
		return HttpResponseRedirect('/newaccount/address')	
	if not signup_status['verification']:
		return HttpResponseRedirect('/newaccount/verification')
	if not signup_status['tos']:
		return HttpResponseRedirect('/newaccount/tos')
	# If reached here, all forms on their end are complete, but still need final verification #
	if not group_handle.verified:
		return HttpResponseRedirect('/newaccount/complete')
	
	return HttpResponseRedirect('/')

### New account step 1 (details) ###
@login_required
def newAccountDetails(request):
	group_handle = request.user.basicuser.group_handle()
	if not hasattr(group_handle,'clinic'):
		return HttpResponseRedirect('/')
	signup_status = clinicSignUpStatus(group_handle)
	gpos = GPO.objects.all() # Grab all GPOS in the database
	size_range = range(1,41) # Used for the inputs to practice size and total number of vets
	return render_to_response('account/sign/newaccount/newaccount_details.html',{'newaccount_details':True,'clinic_status':signup_status,'gpos':gpos,'clinic':group_handle,'size_range':size_range},context_instance=RequestContext(request))

### New account step 2 (address) ###
@login_required
def newAccountAddress(request):
	group_handle = request.user.basicuser.group_handle()
	if not hasattr(group_handle,'clinic'):
		return HttpResponseRedirect('/')
	signup_status = clinicSignUpStatus(group_handle)
	if not signup_status['details']:
		return HttpResponseRedirect('/newaccount/details')
	states = [state.name for state in us.states.STATES] # Generates a list of all 50 states
	return render_to_response('account/sign/newaccount/newaccount_address.html',{'newaccount_address':True,'clinic_status':signup_status,'clinic':group_handle,'states':states},context_instance=RequestContext(request))

### New account step 3 (verification) ###
@login_required
def newAccountVerification(request):
	group_handle = request.user.basicuser.group_handle()
	if not hasattr(group_handle,'clinic'):
		return HttpResponseRedirect('/')
	signup_status = clinicSignUpStatus(group_handle)
	if not signup_status['details']:
		return HttpResponseRedirect('/newaccount/details')
	if not signup_status['address']:
		return HttpResponseRedirect('/newaccount/adress')
	signup_status = clinicSignUpStatus(group_handle)
	states = [state.name for state in us.states.STATES] # Generates a list of all 50 states
	return render_to_response('account/sign/newaccount/newaccount_verification.html',{'newaccount_verification':True,'clinic_status':signup_status,'clinic':group_handle,'states':states},context_instance=RequestContext(request))

### New account step 4 (tos) ###
@login_required
def newAccountTOS(request):
	group_handle = request.user.basicuser.group_handle()
	signup_status = clinicSignUpStatus(group_handle)
	if not hasattr(group_handle,'clinic'):
		return HttpResponseRedirect('/')
	if not signup_status['details']:
		return HttpResponseRedirect('/newaccount/details')
	if not signup_status['address']:
		return HttpResponseRedirect('/newaccount/adress')
	if not signup_status['verification']:
		return HttpResponseRedirect('/newaccount/verification')
	return render_to_response('account/sign/newaccount/newaccount_tos.html',{'newaccount_tos':True,'clinic_status':signup_status,'clinic':group_handle},context_instance=RequestContext(request))

@login_required
def newAccountComplete(request):
	group_handle = request.user.basicuser.group_handle()
	signup_status = clinicSignUpStatus(group_handle)
	if not hasattr(group_handle,'clinic'):
		return HttpResponseRedirect('/')
	for key,value in signup_status.items():
		if value != True:
			return HttpResponseRedirect('/newaccount')
	license = True if (not group_handle.license) else False
	sales = True if (group_handle.sales_no and not group_handle.sales) else False
	return render_to_response('account/sign/newaccount/newaccount_complete.html',{'newaccount_complete':True,'clinic_status':signup_status,'clinic':group_handle,'license':license,'sales':sales},context_instance=RequestContext(request))

### New account step 1 (details) form ###
@login_required
def newAccountDetailsForm(request):
	clinic = request.user.basicuser.group_handle()
	signup_status = clinicSignUpStatus(clinic)
	if request.method == 'POST':
		form = NewAccountDetailsForm(request.POST)
		if form.is_valid():
			clinic.name = form.cleaned_data['name']
			clinic.phonenumber = form.cleaned_data['phonenumber']
			clinic.organization_type = form.cleaned_data['organization_type']
			clinic.number_of_vets = form.cleaned_data['number_of_vets']
			clinic.practice_size = form.cleaned_data['practice_size']
			clinic.website = form.cleaned_data['website']
			large = number_of_vets = form.cleaned_data['large']
			small = number_of_vets = form.cleaned_data['small']
			mixed = number_of_vets = form.cleaned_data['mixed']
			clinic.practice_type = str(large)+";"+str(small)+";"+str(mixed)
			clinic.save()
			return HttpResponseRedirect('/newaccount/address')
		else:
			return HttpResponseRedirect('/newaccount/details')
	else:
		return HttpResponseRedirect('/newaccount/details')

@login_required
def newAccountAddressForm(request):
	clinic = request.user.basicuser.group_handle()
	signup_status = clinicSignUpStatus(clinic)
	if request.method == 'POST':
		form = NewAccountAddressForm(request.POST)
		if form.is_valid():
			address_one = form.cleaned_data['address_one']
			address_two = form.cleaned_data['address_two']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			if not clinic.address: # Make an address object if they do not have one
				address = Address(group = request.user.basicuser.group,
					name = clinic.name,
					address_one=address_one,
					address_two=address_two,
					city=city,
					state = state,
					zipcode = zipcode
					)
				address.save()
				clinic.address = address
			else: # Update their current address object
				address = clinic.address
				address.address_one = address_one
				address.address_two = address_two
				address.city = city
				address.state = state
				address.zipcode = zipcode
				address.save()
			clinic.save()
			return HttpResponseRedirect('/newaccount/verification')
		else:
			return HttpResponseRedirect('/newaccount/address')
	else:
		return HttpResponseRedirect('/newaccount/address')

@login_required
def newAccountVerificationForm(request):
	clinic = request.user.basicuser.group_handle()
	signup_status = clinicSignUpStatus(clinic)
	if request.method == 'POST':
		form = NewAccountVerificationForm(request.POST)
		if form.is_valid():
			clinic.practitioner_name = form.cleaned_data['practitioner_name']
			clinic.license_no = form.cleaned_data['license_no']
			clinic.sales_no = form.cleaned_data['sales_no']
			clinic.save()
			return HttpResponseRedirect('/newaccount/tos')
		else:
			return HttpResponseRedirect('/newaccount/verification')
	else:
		return HttpResponseRedirect('/newaccount/verification')

@login_required
def newAccountTOSForm(request):
	clinic = request.user.basicuser.group_handle()
	signup_status = clinicSignUpStatus(clinic)
	if request.method == 'POST':
		clinic.tos = True
		clinic.save()
		return HttpResponseRedirect("/newaccount")
	else:
		return HttpReponseRedirect("/newaccount/tos")

















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






