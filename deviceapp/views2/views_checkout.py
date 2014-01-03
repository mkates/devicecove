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

##### The cart page #########
def cart(request):
	shoppingcart = getShoppingCart(request)
	shoppingcart_totals = getShoppingCartTotals(shoppingcart)
	dict_one= {'shoppingcart':shoppingcart,'status':400}
	variables = dict(shoppingcart_totals.items() + dict_one.items())
	return render_to_response('account/cart.html',variables,context_instance=RequestContext(request))

##### Add an item to the cart ######
def addToCart(request,itemid):
	#Get or create a shopping cart
	shoppingcart = getShoppingCart(request)
	if not shoppingcart:
		shoppingcart = ShoppingCart()
		shoppingcart.save()
		request.session['shoppingcart'] = shoppingcart.id
	item = Item.objects.get(id=itemid)
	#Only creates the cart object if it doesn't exist
	newCartItem, created = CartItem.objects.get_or_create(shoppingcart=shoppingcart,item=item,quantity=1)
	newCartItem.save()
	return HttpResponseRedirect('/cart')
		
	
##### Update the Cart #########
def updatecart(request):
	item = Item.objects.get(id=request.POST.get('itemid',''))
	method = request.POST.get('method','')
	quantity = request.POST.get('quantity','')
	shoppingcart = getShoppingCart(request)
	if method == 'delete':
		ci = CartItem.objects.get(item=item,shoppingcart=shoppingcart)
		ci.delete()
	if method == 'watchlist':
		if request.user.is_authenticated():
			ci = CartItem.objects.get(item=item,shoppingcart=shoppingcart)
			ci.delete()
			si, created = SavedItem.objects.get_or_create(item=item,user=bu)
			si.save()
		else:
			dict = {'status':600,'redirect':'/login?next=/cart'}
			return HttpResponse(json.dumps(dict), content_type='application/json')
	if method == 'quantity':
		ci = CartItem.objects.get(item=item,shoppingcart=shoppingcart)
		ci.quantity = int(quantity)
		ci.save()
		
	shoppingcart_totals = getShoppingCartTotals(shoppingcart)
	shoppingcart_totals['status']=400
	return HttpResponse(json.dumps(shoppingcart_totals), content_type='application/json')
		
### Landing page once they proceed to checkout ###
def checkoutBegin(request):
	dict = {'checkout_login':True}
	if request.GET.get('e'):
		dict['outcome'] = request.GET.get('e')
	return render_to_response('checkout/checkout_login.html',dict,context_instance=RequestContext(request))

### Login Form to start checkout process ###
def checkoutloginform(request):
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
						return HttpResponseRedirect('checkout/shipping/'+str(checkoutid))
					else:
						return HttpResponseRedirect('checkout/signin?e=wronguser')
				else:
					#User is not logged in, add session items into existing cart and continue
					session_shoppingcart = getShoppingCart(request)
					login(request,user)
					bu = BasicUser.objects.get(user=user)
					for cartitem in session_shoppingcart.cartitem_set.all():
						#Add only items not already in their cart
						if cartitem.item not in bu.shoppingcart.cart_items():
							cartitem.shoppingcart = bu.shoppingcart
							cartitem.save()
					checkoutid = createCheckout(bu)
					return HttpResponseRedirect('checkout/shipping/'+str(checkoutid))
			else:
				return HttpResponseRedirect('checkout/signin?e=userdisabled')		
		else:
			return HttpResponseRedirect('checkout/signin?e=invalidlogin')
	return HttpResponseRedirect('checkout/signin')

### Helper method to create a checkout object for a user ###
def createCheckout(bu):	
	cartitems = bu.shoppingcart.cartitem_set.all()
	checkout = Checkout(buyer=bu,shipping_address=None,payment=None,state=1)
	checkout.save()
	for cartitem in cartitems:
		checkout.cartitem.add(cartitem)
	checkout.save()
	return checkout.id

### Checkout shipping page ###
@login_required
def checkoutShipping(request,checkoutid):
	checkout = Checkout.objects.get(id=checkoutid)
	checkoutValid = checkoutValidCheck(checkout,request)
	dict = {'checkout':checkout}
	if checkoutValid == 200:
		return HttpResponseRedirect('/checkout/signin?e=timeout')
	elif checkoutValid == 300:
		return HttpResponseRedirect('/checkout/signin?e=wronguser')
	elif checkoutValid != 500:
		return HttpResponseRedirect('/checkout/signin')
	return render_to_response('checkout/checkout_shipping.html',dict,context_instance=RequestContext(request))
	
	
	
def checkoutPayment(request,checkoutid):
	if request.user.is_authenticated():
		checkout = Checkout.objects.get(id=checkoutid)
		bu = BasicUser.objects.get(user=request.user)
		if checkout.user == bu:
			return render_to_response('checkout/checkout_payment.html',{},context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/')
	return 
	
def checkoutReview(request,itemid):
	return render_to_response('checkout/checkout_review.html',{},context_instance=RequestContext(request))

def checkoutConfirmation(request,itemid):
	return render_to_response('checkout/checkout_confirmation.html',{},context_instance=RequestContext(request))

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
	for cartitem in shoppingcart.cartitem_set.all():
		count += cartitem.quantity
		totalcost += cartitem.quantity * cartitem.item.price
	return {'total':"$"+"{:,}".format(totalcost),'itemcount':count}

#Validates a checkout request
def checkoutValidCheck(checkout,request):
	# First check if the checkout has already been completed
	if checkout.purchased:
		return 100 # Item already purchased
	# Next check if it has been too long
	time_now = datetime.utcnow().replace(tzinfo=utc)
	time_elapsed = time_now - checkout.start_time
	seconds_elapsed = time_elapsed.seconds
	if seconds_elapsed > 900:
		return 200 # Time Out
	# See if it is the right user
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		if checkout.buyer != bu:
			return 300 # Incorrect user
	else:
		return 400 #User not logged in at all
	return 500 #Checkout is VALID!!!
