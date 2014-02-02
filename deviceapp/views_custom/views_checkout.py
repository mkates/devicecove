from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
from deviceapp.forms import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import views_payment as payment_view
import views_email	as email_view
import json
import re
from datetime import datetime
from django.utils.timezone import utc
import balanced


###################################
### Sign Up Form ##################
###################################
# When a user is created, create the following: User, BasicUser, Shopping Cart
# Then, transfer all the items from the session shopping cart to their account
# Finally, create a Checkout if the user is checking out
def newuserform(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():		
			# General user sign-up
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			zipcode = form.cleaned_data['zipcode']
			password = form.cleaned_data['password']
			checkout_signup = form.cleaned_data['checkout_signup']
			#If user email is already used, serve an email error
			if User.objects.filter(username=email).exists():
				return render_to_response('account/login.html',{'error':'email'},context_instance=RequestContext(request))
			
			# Create new user
			newuser = User.objects.create_user(email,email,password)
			newuser.save()
			
			# Create the basic user
			nbu = BasicUser(user=newuser,name=name,email=email,zipcode=zipcode)
			nbu.save()
			
			# Attempt to get the lat long and assign the city, state, and county
			try:
				latlong_obj = LatLong.objects.get(zipcode=int(zipcode))
				nbu.city = latlong_obj.city
				nbu.county = latlong_obj.county
				nbu.state = latlong_obj.state
				nbu.save()
			except:
				latlong_obj = None
			
			# Create the shopping cart
			shoppingcart = ShoppingCart(user=nbu)
			shoppingcart.save()
			
			user = authenticate(username=newuser,password=password)
			
			# Add all session cart items into their account's shopping cart
			session_shoppingcart = getShoppingCart(request)
			if session_shoppingcart:
				for cartitem in session_shoppingcart.cartitem_set.all():
					cartitem.shoppingcart = nbu.shoppingcart
					cartitem.save()	
			
			# Send welcome email 
			email_view.composeEmailWelcome(request,nbu)
			
			#Login, now that cart items from session are added to the user account
			login(request,user)
			
			# If checking out. . . 
			if checkout_signup:
				checkoutid = createCheckout(nbu)
				return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))

			# If it was a login wall . . .
			if request.GET.get('next',''):
				return HttpResponseRedirect(request.GET.get('next','/'))
			
			# Else just send them to their profile
			return HttpResponseRedirect('/account/profile')
		else:
			return render_to_response('account/login.html',{'error':'invalid'},context_instance=RequestContext(request))
	return HttpResponseRedirect('/error/notpost')
	
	
###################################
### General Cart Functions ########
###################################

##### The cart page #########
def cart(request):
	# Retrieves the ShoppingCart
	shoppingcart = getShoppingCart(request)
	#Calculates price and counts from the ShoppingCart
	shoppingcart_totals = getShoppingCartTotals(shoppingcart)
	# Create the variables dictionary
	dict = shoppingcart_totals
	dict['shoppingcart'] = shoppingcart
	return render_to_response('account/cart.html',dict,context_instance=RequestContext(request))

##### Add an item to the cart ######
def addToCart(request,itemid):
	if request.method == "POST":
		# Get or create a shopping cart
		shoppingcart = getShoppingCart(request)
		if not shoppingcart:
			shoppingcart = ShoppingCart()
			shoppingcart.save()
			request.session['shoppingcart'] = shoppingcart.id
		item = Item.objects.get(id=itemid)
		# Only creates the cart object if it doesn't exist
		newCartItem, created = CartItem.objects.get_or_create(shoppingcart=shoppingcart,item=item,price=item.price,quantity=1)
		newCartItem.save()
		return HttpResponseRedirect('/cart')
	return HttpResponseRedirect('/cart')
	
##### Update the Cart Wishlist #########
def updateCartWishlist(request,cartitemid):
	cartitem = CartItem.objects.get(id=cartitemid)
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		cartitem.shoppingcart = None
		cartitem.delete()
		si, created = SavedItem.objects.get_or_create(item=cartitem.item,user=bu)
		si.save()
		return HttpResponseRedirect('/cart')
	else:
		return HttpResponseRedirect('/login?next=/cart')
		
##### Delete Cart Item #########
def updateCartDelete(request,cartitemid):
	cartitem = CartItem.objects.get(id=cartitemid)
	shoppingcart = getShoppingCart(request)
	if cartitem.shoppingcart == shoppingcart: #Only if its the right shopping cart
		cartitem.shoppingcart = None
		cartitem.delete()
	return HttpResponseRedirect('/cart')

##### Update Cart Quantity #########
def updateCartQuantity(request,cartitemid):
	cartitem = CartItem.objects.get(id=cartitemid)
	shoppingcart = getShoppingCart(request)
	if cartitem.shoppingcart == shoppingcart:
		cartitem.quantity = int(request.POST['quantity'])
		cartitem.save()
	return HttpResponseRedirect('/cart')
	
###################################
### Confirm User In Checkout ######
###################################

# ### Landing page once they proceed to checkout ###
def checkoutVerify(request):
	return render_to_response('checkout/checkout_login.html',{'checkout_verify':True},context_instance=RequestContext(request))

### Landing page if there is an error ####
def checkoutVerifyError(request,error):
	# This variable is a boolean in the signup form to know you are checking out
	dict = {'checkout_verify':True}
	#Write up your error message
	errormessage = 'There was an error verifying your account. Please try again'
	if error == 'username_password_error':
		errormessage = 'Oops! Your username and password do not match'
	if error == 'disabled_account':
		errormessage = 'Your account has been disabled. Please contact us if you would like it reactivated'
	if error == 'different_user':
		errormessage = 'You are currently logged in as a different user'
	if error == 'timeout':
		errormessage = 'Your checkout session timed out'
	if error == 'purchased':
		errormessage = 'You already purchased the items in this cart'
	if error == 'emptycart':
		errormessage = 'You have no items in your shopping cart'
	if error == 'notloggedin':
		errormessage = 'You are not currently logged in'
	if error == 'toolarge':
		errormessage = 'The items in your cart cannot exceed $15,000'
	if error == 'payment':
		errormessage = 'There was a problem processing your payment selection'
	dict['error'] = errormessage
	return render_to_response('checkout/checkout_login.html',dict,context_instance=RequestContext(request))

### Login Form to start checkout process ###
def checkoutlogin(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():	
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			rememberme = form.cleaned_data['rememberme']
			user = authenticate(username=email,password=password)
			if user is not None:
				if user.is_active:
					if request.user.is_authenticated():
						# If a user is already logged in, login must match
						if user == request.user:
							bu = BasicUser.objects.get(user=request.user)
							checkoutid = createCheckout(bu)
							return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
						else:
							return HttpResponseRedirect('/checkout/verify/different_user')
					else:
						# User is not logged in, add session items into existing cart and continue
						session_shoppingcart = getShoppingCart(request)
						login(request,user)
						if rememberme:
							request.session.set_expiry(500000)
						else:
							request.session.set_expiry(0)
						bu = BasicUser.objects.get(user=user)
						if session_shoppingcart:
							for cartitem in session_shoppingcart.cartitem_set.all():
								#Add only items not already in their cart
								if cartitem.item not in bu.shoppingcart.cart_items():
									cartitem.shoppingcart = bu.shoppingcart
									cartitem.save()
						checkoutid = createCheckout(bu)
						return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
				else:
					return HttpResponseRedirect('/checkout/verify/disabled_account')
			else:
				return HttpResponseRedirect('/checkout/verify/username_password_error')		
	return HttpResponseRedirect('/checkout/verify/error')

### Helper method to create a checkout object for a user ###
### Adds each item from the BU into the checkout cart
def createCheckout(bu):	
	cartitems = bu.shoppingcart.cartitem_set.all()
	checkout = Checkout(buyer=bu,shipping_address=None,state=1)
	checkout.save()
	for cartitem in cartitems:
		if cartitem.item.liststatus == 'active':
			cartitem.checkout = checkout
			cartitem.price = cartitem.item.price
			cartitem.save()
	return checkout.id

###################################
### Checkout Shipping #############
###################################

### Checkout shipping page ###
@login_required
def checkoutShipping(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	return render_to_response('checkout/checkout_shipping.html',{'checkout':checkout},context_instance=RequestContext(request))

@login_required
def	useAddress(request):
	if request.method == 'POST':
		checkoutid = request.POST['checkout_id']
		addressid = request.POST['address_id']
		# Checkout Validation
		checkout = Checkout.objects.get(id=checkoutid)
		checkoutValid = checkoutValidCheck(checkout,request)
		if checkoutValid['status'] != 201:
			return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
		#Set the address of the checkout to the Address
		checkout = Checkout.objects.get(id=checkoutid)
		address = Address.objects.get(id=addressid)
		checkout.shipping_address = address
		checkout.state = 2
		checkout.save()
		return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))
	return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))

@login_required
def deleteAddress(request):
	if request.method == 'POST':
		checkoutid = request.POST['checkout_id']
		addressid = request.POST['address_id']
		# Checkout Validation
		checkout = Checkout.objects.get(id=checkoutid)
		checkoutValid = checkoutValidCheck(checkout,request)
		if checkoutValid['status'] != 201:
			return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
		# Grab a handle for the address to delete
		deleteaddress = Address.objects.get(id=addressid)
		# Remove the address object from the user
		if checkout.shipping_address == deleteaddress:
			checkout.shipping_address = None
			checkout.save()
		payment_view.deleteAddress(request,deleteaddress)		
		return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
	return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))

@login_required
def newAddress(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	if request.method == 'POST':
		#Create the Address object
		user = request.user.basicuser
		name = request.POST['name']
		address_one = request.POST['address_one']
		address_two = request.POST.get('address_two','')
		city = request.POST['city']
		state = request.POST['state']
		zipcode = request.POST['zipcode']
		phonenumber = request.POST['phonenumber']
		newaddress = Address(user=user,name=name,address_one=address_one,address_two=address_two,city=city,state=state,zipcode=zipcode,phonenumber=phonenumber)
		newaddress.save()
		#Create new payment object as well
		new_payment = CheckAddress(user=user,address=newaddress)
		new_payment.save()
		#Point checkout's address to the new Address
		checkout = Checkout.objects.get(id=checkoutid)
		checkout.shipping_address = newaddress
		checkout.state = 2
		checkout.save()
		return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))
	return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))

		
###################################
### Checkout Payment ##############
###################################	
@login_required
def checkoutPayment(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	payment_methods = False
	for payment in request.user.basicuser.payment_set.all():
		if hasattr(payment,'balancedbankaccount') or hasattr(payment,'balancedcard'):
			payment_methods = True
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	elif checkout.shipping_address == None:
		return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
	return render_to_response('checkout/checkout_payment.html',{'checkout':checkout,'payment_methods':payment_methods},context_instance=RequestContext(request))

@login_required
def checkoutUsePayment(request,checkoutid,paymentid):
	if request.method == 'POST':
		# Checkout Validation
		checkout = Checkout.objects.get(id=checkoutid)
		checkoutValid = checkoutValidCheck(checkout,request)
		if checkoutValid['status'] != 201:
			return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])	
		payment = Payment.objects.get(id=paymentid)
		if not payment.user == request.user.basicuser:
			return HttpResponseRedirect('/checkout/verify/payment')	
		checkout.payment = payment
		checkout.save()
		return HttpResponseRedirect('/checkout/review/'+str(checkoutid))
	return HttpResponseRedirect('/checkout/review/'+str(checkoutid))
	
@login_required
def checkoutDeletePayment(request,checkoutid,paymentid):
	if request.method == 'POST':
		# Checkout Validation
		checkout = Checkout.objects.get(id=checkoutid)
		checkoutValid = checkoutValidCheck(checkout,request)
		if checkoutValid['status'] != 201:
			return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
		payment = Payment.objects.get(id=paymentid)
		if 	checkout.payment == payment:
			checkout.payment = None
			checkout.save()
		# Safely de-references the payment
		dp = payment_view.deletePayment(request,paymentid)
		return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))
	return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))
	
@login_required
def checkoutAddCard(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	# Add credit card to a Basic User
	balancedCard = payment_view.addBalancedCard(request)
	if balancedCard['status'] == 201:
		checkout.payment = balancedCard['card']
		checkout.save()	
	return HttpResponse(json.dumps({'status':balancedCard['status'],'error':balancedCard['error']}), content_type='application/json')

@login_required
def checkoutAddBankAccount(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	# Add bank account to checkout
	balancedBankAccount = payment_view.addBalancedBankAccount(request)
	if balancedBankAccount['status'] == 201:
		checkout.payment = balancedBankAccount['bank']
		checkout.save()	
	return HttpResponse(json.dumps({'status':balancedBankAccount['status'],'error':balancedBankAccount['error']}), content_type='application/json')
	
###################################
### Checkout Review  ##############
###################################
@login_required
def checkoutReview(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	if not checkout.shipping_address:
		return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
	elif checkout.shipping_address.user != request.user.basicuser:
		checkout.shipping_address = None
		checkout.save()
		return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
	elif checkout.payment == None:
		return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))
	error = allItemsAvailable(checkout)
	return render_to_response('checkout/checkout_review.html',{'checkout':checkout,'error':error},context_instance=RequestContext(request))

@login_required
def checkoutDeleteItem(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	cartitemid = request.POST['checkoutitemid']
	cartitem = CartItem.objects.get(id=cartitemid)
	cartitem.delete()
	return HttpResponseRedirect('/checkout/review/'+str(checkoutid))

@login_required
def checkoutMoveToSaved(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	cartitemid = request.POST['checkoutitemid']
	cartitem = CartItem.objects.get(id=cartitemid)
	#Add to Saved Items
	bu = BasicUser.objects.get(user=request.user)
	si, created = SavedItem.objects.get_or_create(item=cartitem.item,user=bu)
	si.save()
	#Delete the CartItem
	cartitem.delete()
	return HttpResponseRedirect('/checkout/review/'+str(checkoutid))

@login_required
def checkoutChangeQuantity(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	cartitemid = request.POST['checkoutitemid']
	cartitem = CartItem.objects.get(id=cartitemid)
	#Update Quantity
	cartitem.quantity = int(request.POST['item-quantity'])
	cartitem.save()
	return HttpResponseRedirect('/checkout/review/'+str(checkoutid))

###################################
### Checkout Purchase #############
###################################
@login_required
def checkoutPurchase(request,checkoutid):
	# 1. Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	
	# 2. Make sure all the items are still available
	notavailable = allItemsAvailable(checkout)
	if notavailable:
		return render_to_response('checkout/checkout_review.html',{'checkout':checkout,'error':notavailable},context_instance=RequestContext(request))
	
	# 3. Make purchase
	try:
		bu = BasicUser.objects.get(user=request.user)
		if hasattr(checkout.payment,'balancedcard'):
			uri = checkout.payment.balancedcard.uri
		else:
			uri = checkout.payment.balancedbankaccount.uri
		balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
		customer = balanced.Customer.find(bu.balanceduri)
		amount = checkout.total()
		cd = customer.debit(appears_on_statement_as="Vet Cove",amount=amount,source_uri=uri)
		print cd
		if cd.status != "succeeded":
			print 'here'
			raise Exception("Charge Failed")
	except Exception,e:
		return render_to_response('checkout/checkout_review.html',{'checkout':checkout,'error':e},context_instance=RequestContext(request))
	
	# 4. Update Items in the system, delete cart-items create Purchased Objects
	for cartitem in checkout.cartitem_set.all():
		item = cartitem.item
		if item.quantity == cartitem.quantity:
			item.liststatus = 'sold'
			item.quantity = 0
		elif item.quantity > cartitem.quantity:
			item.quantity -= cartitem.quantity
		item.save()
		amount = cartitem.price * cartitem.quantity
		pi = PurchasedItem(seller=item.user,
						buyer=bu,
						cartitem=cartitem,
						unit_price=cartitem.price,
						checkout=cartitem.checkout,
						total=amount,
						item_name=cartitem.item.name,
						quantity=cartitem.quantity,
						payment=checkout.payment)
		pi.save()
		cartitem.shoppingcart = None
		cartitem.save()
		# Email the seller of the item
		email_view.composeEmailItemSold_Seller(request,bu,pi)

	# 5. Mark checkout object as purchased
	checkout.purchased = True
	checkout.purchased_time = datetime.utcnow().replace(tzinfo=utc)
	checkout.save()
	
	# 6. Email confirmation
	email_view.composeEmailItemPurchased_Buyer(request,bu,checkout)
	
	return HttpResponseRedirect('/checkout/confirmation/'+str(checkout.id))
	
###################################
### Checkout Confirmation##########
###################################
@login_required
def checkoutConfirmation(request,checkoutid):
	checkout = Checkout.objects.get(id=checkoutid)
	if checkout.buyer == request.user.basicuser:
		return render_to_response('checkout/checkout_confirmation.html',{'checkout':checkout},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/cart')

####################################################
###### Checkout Helper Methods #####################
####################################################


#Get the shopping cart from the user, the session, or return none
def getShoppingCart(request):
	shoppingcart = None
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		shoppingcart = ShoppingCart.objects.get(user=bu)
	else:
		if 'shoppingcart' in request.session:
			shoppingcart = ShoppingCart.objects.get(id=int(request.session['shoppingcart']))
	return shoppingcart

#Calculate the total cost and number of items in a shopping cart
def getShoppingCartTotals(shoppingcart):
	count = 0
	totalcost = 0
	if shoppingcart:
		for cartitem in shoppingcart.cartitem_set.all():
			count += cartitem.quantity
			totalcost += cartitem.quantity * cartitem.item.price
	return {'total':"$"+"{:,}".format(totalcost),'itemcount':count}

#Checks if all items are available, and updates checkout accordingly
def allItemsAvailable(checkout):
	changed = False
	for cartitem in checkout.cartitem_set.all():
		if cartitem.item.liststatus != "active":
			cartitem.checkout = None
			cartitem.save()
			changed = True
		elif cartitem.item.quantity < cartitem.item.quantity:
			checkout.cartitem.quantity = cartitem.item.quantity
			changed = True
	if changed:
		return 'Some items in your cart are no longer available. Your cart has been updated'
	else:
		return None
	
#### Validates a current checkout and request #######
### Checks (1) checkout completed, (2) timeout, (3) Right User, (4) Not empty shopping cart
### (5) Under Balanced Charge Limit
# Returns '500'-> success or '100'->failure
def checkoutValidCheck(checkout,request):
	dict = None
	
	# First check if the checkout has already been completed
	if checkout.purchased:
		dict = {'status':100,'error':'purchased'}
	
	# Next check if it has been too long
	time_now = datetime.utcnow().replace(tzinfo=utc)
	time_elapsed = time_now - checkout.start_time
	seconds_elapsed = time_elapsed.seconds
	if seconds_elapsed > 9000:
		dict = {'status':100,'error':'timeout'}
	
	# See if it is the right user
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		if checkout.buyer != bu:
			dict = {'status':100,'error':'different_user'} # Incorrect user
	else:
		dict = {'status':100,'error':'notloggedin'} #User not logged in at all
	
	#If the user's shoppingcart is empty
	if not checkout.cartitem_set.all():
		dict = {'status':100,'error':'emptycart'} # Empty Shopping Cart
	if dict:
		dict['checkout'] = checkout
		return dict
	
	#If the cart is under $15,000
	if int(checkout.total()) > 1499999:
		dict = {'status':100,'error':'toolarge'} # Too expensive
	
	if not dict:	
		dict = {'status':201} #Checkout is VALID!!!
	
	return dict
