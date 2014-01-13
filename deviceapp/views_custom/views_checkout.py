from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import json
from datetime import datetime
from django.utils.timezone import utc
import balanced


###################################
### Sign Up Form ##################
###################################


# When a user is created, create the following: User, BasicUser, Shopping Cart, UserAddress
# Then, transfer all the items from the session shopping cart to their account
# Finally, create a Checkout if the user is checking out
def newuserform(request):
	if request.method == 'POST':
		try:
			# Extract all sign up data
			businesstype = request.POST['businesstype']
			company = request.POST.get('company','')
			name = request.POST['name']
			email = request.POST['email']
			#If user email is already in user, go to signup + email error
			if User.objects.filter(username=email).count():
				return HttpResponseRedirect("/signup?e=email")
			address_one = request.POST['address_one']
			address_two = request.POST.get('address_two','')
			zipcode = request.POST['zipcode']
			city = request.POST['city']
			state = request.POST['state']
			website = request.POST.get('website','')
			phonenumber = request.POST['phonenumber']
			password = request.POST['password']
			newuser = User.objects.create_user(email,email,password)
			newuser.save()
			
			# Create the basic user
			nbu = BasicUser(user=newuser,name=name,businesstype=businesstype,company=company,email=email,address_one=address_one,address_two=address_two,zipcode=zipcode,city=city,
			state=state,website=website,phonenumber=phonenumber)
			nbu.save()
			
			# Create the shopping cart
			shoppingcart = ShoppingCart(user=nbu)
			shoppingcart.save()
			#Create a user address
			address = UserAddress(user=nbu,name=name,address_one=address_one,address_two=address_two,city=city,state=state,zipcode=zipcode,phonenumber=phonenumber)
			address.save()
			user = authenticate(username=newuser,password=password)
			
			# Add all session cart items into their account's shopping cart
			session_shoppingcart = getShoppingCart(request)
			for cartitem in session_shoppingcart.cartitem_set.all():
				cartitem.shoppingcart = nbu.shoppingcart
				cartitem.save()
				
			# Add all the items from the BU shopping cart into Checkout object
			# All items should reamin in the BU shopping as well!
			if request.POST['checkoutsignin']:
				checkoutid = createCheckout(nbu)
				login(request,user)
				return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
			
			#If user is not checking out, send them back to the homepage
			login(request,user)
			return HttpResponseRedirect('/')
			
		except Exception,e:
			# Any sign up errors go the error page
			return HttpResponseRedirect('/error/signup')
	# They called this method as a GET, its a hacker or im a bad developer, TBD
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
	#Create the variables dictionary
	dict = shoppingcart_totals
	dict['shoppingcart'] = shoppingcart
	return render_to_response('account/cart.html',dict,context_instance=RequestContext(request))

##### Add an item to the cart ######
def addToCart(request,itemid):
	# Get or create a shopping cart
	shoppingcart = getShoppingCart(request)
	if not shoppingcart:
		shoppingcart = ShoppingCart()
		shoppingcart.save()
		request.session['shoppingcart'] = shoppingcart.id
	item = Item.objects.get(id=itemid)
	# Only creates the cart object if it doesn't exist
	newCartItem, created = CartItem.objects.get_or_create(shoppingcart=shoppingcart,item=item,quantity=1)
	newCartItem.save()
	return HttpResponseRedirect('/cart')
	
##### Update the Cart #########
def updatecart(request):
	item = Item.objects.get(id=request.POST.get('itemid',''))
	method = request.POST.get('method','')
	quantity = request.POST.get('quantity','')
	shoppingcart = getShoppingCart(request)
	# If deleting an item from the cart
	if method == 'delete':
		ci = CartItem.objects.get(item=item,shoppingcart=shoppingcart)
		ci.delete()
	# If moving the item to the watchlist
	if method == 'watchlist':
		if request.user.is_authenticated():
			bu = BasicUser.objects.get(user=request.user)
			ci = CartItem.objects.get(item=item,shoppingcart=shoppingcart)
			ci.delete()
			si, created = SavedItem.objects.get_or_create(item=item,user=bu)
			si.save()
		else:
			dict = {'status':600,'redirect':'/login?next=/cart'}
			return HttpResponse(json.dumps(dict), content_type='application/json')
	# If changing the quantity of an item
	if method == 'quantity':
		ci = CartItem.objects.get(item=item,shoppingcart=shoppingcart)
		ci.quantity = int(quantity)
		ci.save()	
	shoppingcart_totals = getShoppingCartTotals(shoppingcart)
	shoppingcart_totals['status']=400 #400 is a success for the method
	return HttpResponse(json.dumps(shoppingcart_totals), content_type='application/json')

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
	dict['error'] = errormessage
	return render_to_response('checkout/checkout_login.html',dict,context_instance=RequestContext(request))

### Login Form to start checkout process ###
def checkoutlogin(request):
	if request.method == "POST":
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				if request.user.is_authenticated():
					#If a user is already logged in, login must match
					if user == request.user:
						bu = BasicUser.objects.get(user=request.user)
						checkoutid = createCheckout(bu)
						return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
					else:
						return HttpResponseRedirect('/checkout/verify/different_user')
				else:
					#User is not logged in, add session items into existing cart and continue
					session_shoppingcart = getShoppingCart(request)
					login(request,user)
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
	checkout = Checkout(buyer=bu,shipping_address=None,payment=None,state=1)
	checkout.save()
	for cartitem in cartitems:
		checkout.cartitem.add(cartitem)
	checkout.save()
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
		#Set the address of the checkout to the UserAddress
		checkout = Checkout.objects.get(id=checkoutid)
		address = UserAddress.objects.get(id=addressid)
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
		deleteaddress = UserAddress.objects.get(id=addressid)
		#Reset the checkout references to prevent delete propagation
		if checkout.shipping_address == deleteaddress:
			checkout.shipping_address = None
			checkout.save()
		deleteaddress.delete()
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
		#Create the UserAddress object
		user = BasicUser.objects.get(user=request.user)
		name = request.POST['name']
		address_one = request.POST['address_one']
		address_two = request.POST.get('address_two','')
		city = request.POST['city']
		state = request.POST['state']
		zipcode = request.POST['zipcode']
		phonenumber = request.POST['phonenumber']
		newaddress = UserAddress(user=user,name=name,address_one=address_one,address_two=address_two,city=city,state=state,zipcode=zipcode,phonenumber=phonenumber)
		newaddress.save()
		#Point checkout's address to the new UserAddress
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
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	elif checkout.shipping_address == None:
		return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
	return render_to_response('checkout/checkout_payment.html',{'checkout':checkout},context_instance=RequestContext(request))

@login_required
def	usePayment(request):
	if request.method == 'POST':
		checkoutid = request.POST['checkout_id']
		paymentid = request.POST['payment_id']
		# Checkout Validation
		checkout = Checkout.objects.get(id=checkoutid)
		checkoutValid = checkoutValidCheck(checkout,request)
		if checkoutValid['status'] != 201:
			return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])	
		#Set the payment of the checkout to the BalancedCard
		checkout = Checkout.objects.get(id=checkoutid)
		payment = BalancedCard.objects.get(id=paymentid)
		checkout.payment = payment
		checkout.state = 3
		checkout.save()
		return HttpResponseRedirect('/checkout/review/'+str(checkoutid))
	
@login_required
def deletePayment(request):
	if request.method == 'POST':
		checkoutid = request.POST['checkout_id']
		paymentid = request.POST['payment_id']
		# Checkout Validation
		checkout = Checkout.objects.get(id=checkoutid)
		checkoutValid = checkoutValidCheck(checkout,request)
		if checkoutValid['status'] != 201:
			return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])	
		# Grab a handle for the address to delete
		deletecard = BalancedCard.objects.get(id=paymentid)
		#Reset the checkout references to prevent delete propagation
		if checkout.payment == deletecard:
			checkout.payment = None
			checkout.save()
		deletecard.delete()
		return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))
	return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))

@login_required
def addCreditCard(request,checkoutid):
	# Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	# Add credit card to a Basic User
	balanced_addCard = addBalancedCard(request)
	if balanced_addCard['status'] == 201:
		checkout.payment = balanced_addCard['card']
		checkout.save()	
	return HttpResponse(json.dumps({'status':balanced_addCard['status'],'error':balanced_addCard['error']}), content_type='application/json')

#Adds a balanced CC and get or creates a BU's Customer URI
def addBalancedCard(request):
	uri = request.POST.get('uri','')
	brand = request.POST.get('brand','')
	cardhash = request.POST.get('hash','')
	expiration_month = request.POST.get('expiration_month','')
	expiration_year = request.POST.get('expiration_year','')
	last_four = request.POST.get('last_four','')
	try:
		# Configure Balanced API
		balanced.configure(settings.BALANCED_API_KEY)
		# Either find or get the Balanced Customer
		bu = BasicUser.objects.get(user=request.user)
		# See if user has a balanced account
		if bu.balanceduri:
			customer = balanced.Customer.find(bu.balanceduri)
		# If not, create a Balanced Customer and update BU Profile
		else:
			customer = balanced.Customer(name=bu.name,email=bu.email,phone=bu.phonenumber).save()
			bu.balanceduri = customer.uri
			bu.save()
		# If card not already saved, add the card to the customer and add the card to the database
		if not doesCardExist(bu,cardhash):
			customer.add_card(uri)
			new_card = BalancedCard(user=bu,card_uri=uri,brand=brand,cardhash=cardhash,expiration_month=expiration_month,expiration_year=expiration_year,last_four=last_four)
			new_card.save()
			#If the only credit card, set is as the default
			if not bu.default_cc:
				bu.default_cc = new_card
				bu.save()
			return {'status':201,'card':new_card,'error':'None'} # Success
		return {'status':500,'error':'Card Already Saved'} # Card Already Saved
	except Exception,e:
		return {'status':500,'error':e} # Failure

#Helper method to see if the card hash already exists
@login_required
def doesCardExist(bu,hash):
	cards = bu.balancedcard_set.all();
	for card in cards:
		if card.cardhash == hash:
			return True
	return False	
	
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
	print 'started'
	# 1. Checkout Validation
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	if checkoutValid['status'] != 201:
		return HttpResponseRedirect('/checkout/verify/'+checkoutValid['error'])
	
	# 2. Make sure all the items are still available
	notavailable = allItemsAvailable(checkout)
	if notavailable:
		return render_to_response('checkout/checkout_review.html',{'checkout':checkout,'error':available},context_instance=RequestContext(request))
	
	# 3. Make purchase
	try:
		bu = BasicUser.objects.get(user=request.user)
		card_uri = checkout.payment.card_uri
		balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
		customer = balanced.Customer.find(bu.balanceduri)
		amount = checkout.total()*100
		customer.debit(appears_on_statement_as="Vet Cove",amount=amount,source_uri=card_uri)
	except:
		return render_to_response('checkout/checkout_review.html',{'checkout':checkout,'error':'There was an error charging your credit card'},context_instance=RequestContext(request))
	
	# 4. Update Items in the system, delete cart-items create Purchased Objects
	for cartitem in checkout.cartitem.all():
		item = cartitem.item
		if item.quantity == cartitem.quantity:
			item.liststatus = 'sold'
			item.quantity = 0
		elif item.quantity > cartitem.quantity:
			item.quantity -= cartitem.quantity
		item.save()
		pi = PurchasedItem(seller=item.user,buyer=bu,item=cartitem.item,quantity=cartitem.quantity)
		pi.save()
		cartitem.shoppingcart = None
		cartitem.save()
		
	# 5. Mark checkout object as purchased
	checkout.purchased = True
	checkout.save()
		
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
	for cartitem in checkout.cartitem.all():
		if cartitem.item.liststatus != "active":
			checkout.cartitem.remove(cartitem)
			checkout.save()
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
	if not checkout.cartitem.all():
		dict = {'status':100,'error':'emptycart'} # Incorrect user
	if dict:
		dict['checkout'] = checkout
		return dict
	return {'status':201} #Checkout is VALID!!!
