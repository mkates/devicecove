from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.cache import cache
import json, re, random, string
from datetime import datetime
from django.utils.timezone import utc
import balanced
from helper.model_imports import *

###################################
### General Cart Functions ########
###################################

##### The cart page #########
@login_required
def cart(request):
	shoppingcart = request.user.basicuser.clinic.shoppingcart
	cartitems = shoppingcart.cartitem_set.all()
	cartitems_l = []
	for i in range(3):
		cartitems_l.append(cartitems[0])
	shoppingcart_totals = getShoppingCartTotals(shoppingcart)
	return render_to_response('account/pages/cart.html',{'totals':shoppingcart_totals,'cartitems':cartitems_l},context_instance=RequestContext(request))

##### Add an item to the cart ######
@login_required
def addToCart(request,itemid):
	if request.method == "POST":
		item_id = request.POST.get('itemid',None)
		quantity = request.POST.get('quantity',1)
		address = request.POST.get('address',None)
		item = Item.objects.get(id=item_id)
		cartitem = CartItem(shoppingcart=request.user.clinic.shoppingcart,item=item,address=address,quantity=quantity)
		cartitem.save()
	return HttpResponseRedirect('/cart')

##### Update the Cart Wishlist #########
@login_required
def updateCartWishlist(request,cartitemid):
	cartitem = CartItem.objects.get(id=cartitemid)
	if request.method == "POST":
		clinic = request.user.basicuser.clinic
		cartitem.shoppingcart = None
		cartitem.delete()
		si, created = SavedItem.objects.get_or_create(item=cartitem.item,clinic=clinic)
		si.save()
	return HttpResponseRedirect('/cart')
		
##### Delete Cart Item #########
def updateCartDelete(request,cartitemid):
	cartitem = CartItem.objects.get(id=cartitemid)
	if request.method == "POST":
		cartitem.shoppingcart = None
		cartitem.delete()
	return HttpResponseRedirect('/cart')

##### Update Cart Quantity #########
def updateCartQuantity(request,cartitemid):
	cartitem = CartItem.objects.get(id=cartitemid)
	if request.method == "POST":
		quantity = request.POST.get('quantity',1)
		cartitem.quantity = quantity
		cartitem.save()
	return HttpResponseRedirect('/cart')

####################################################
###### Checkout Helper Methods #####################
####################################################

# Calculate the total cost and number of items in a shopping cart
def getShoppingCartTotals(shoppingcart):
	items = 0
	products = 0
	totalcost = 0
	if shoppingcart:
		for cartitem in shoppingcart.cartitem_set.all():
			items += cartitem.quantity
			products += 1
			totalcost += cartitem.quantity * cartitem.inventory.base_price
	return {'total':"$"+"{:,}".format(totalcost),'items_count':items,'products_count':products}



###################################
### Checkout Shipping #############
###################################

@login_required
def newAddress(request):
	if request.method == 'POST':
		# Create the Address object
		clinic = request.user.basicuser.clinic
		name = request.POST['name']
		address_one = request.POST['address_one']
		address_two = request.POST.get('address_two','')
		city = request.POST['city']
		state = request.POST['state']
		zipcode = request.POST['zipcode']
		newaddress = Address(clinic=clinic,name=name,address_one=address_one,address_two=address_two,city=city,state=state,zipcode=zipcode)
		newaddress.save()
	return HttpResponseRedirect('/cart')

		
###################################
### Checkout Payment ##############
###################################	

@login_required
def checkoutPayment(request,checkoutid):
	clinic = request.user.basicuser.clinic
	for payment in clinic.payment_set.all():
		if hasattr(payment,'balancedbankaccount') or hasattr(payment,'balancedcard') or hasattr(payment,'checkpayment'):
			payment_methods = True
	return render_to_response('checkout/checkout_payment.html',{'checkout':checkout,'payment_methods':payment_methods,'paying':True,'BALANCED_MARKETPLACE_ID':settings.BALANCED_MARKETPLACE_ID},context_instance=RequestContext(request))

@login_required
def checkoutAddCard(request,checkoutid):
	balancedCard = addBalancedCard(request)
	if balancedCard['status'] == 201:	
		return HttpResponse(json.dumps({'status':balancedCard['status'],'error':balancedCard['error']}), content_type='application/json')

### Currently Not Used At This Point ###
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
	if checkout.shipping_address == None and checkout.shippingAddressRequired():
		return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
	if checkout.shipping_address:
		if checkout.shipping_address.user != request.user.basicuser:
			checkout.shipping_address = None
			checkout.save()
			return HttpResponseRedirect('/checkout/shipping/'+str(checkoutid))
	elif checkout.payment == None:
		return HttpResponseRedirect('/checkout/payment/'+str(checkoutid))
	error = allItemsAvailable(checkout)
	checkout.save()
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

###################################
### Checkout Purchase #############
###################################
@login_required
def checkoutPurchase(request,checkoutid):
	bu = request.user.basicuser
	
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
		if not hasattr(checkout.payment,'checkpayment'): # Only charge if its a bank account or cc
			if hasattr(checkout.payment,'balancedcard'):
				uri = checkout.payment.balancedcard.uri
			elif hasattr(checkout.payment,'balancedbankaccount'):
				uri = checkout.payment.balancedbankaccount.uri
			balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
			customer = balanced.Customer.find(bu.balanceduri)
			amount = checkout.total()
			cd = customer.debit(appears_on_statement_as="Vet Cove",amount=amount,source_uri=uri)
			if not cd.status == "succeeded":
				raise Exception("Failed to Complete Transaction")
	except Exception,e:
		return render_to_response('checkout/checkout_review.html',{'checkout':checkout,'error':e},context_instance=RequestContext(request))
	
	# 4. Update Items in the system, delete cart-items create Purchased Objects
	order = Order(buyer=bu,payment=checkout.payment,item_total=checkout.subtotal(),credits=checkout.credit_discount(),shipping_address=checkout.shipping_address,transaction_number=cd.transaction_number)
	order.save()
	for cartitem in checkout.cartitem_set.all():
		item = cartitem.item
		item_handle = item.item_handle()
		# Update item quantity and status (if applicable)
		if item.item_type() != 'usedequipment':
			if item_handle.quantity == cartitem.quantity:
				item_handle.liststatus = 'sold'
				item_handle.quantity = 0
			elif item_handle.quantity > cartitem.quantity:
				item_handle.quantity -= cartitem.quantity
			item_handle.save()
		else:
			item_handle.liststatus = 'sold'
			item_handle.sold_online = True
		item_handle.save()
		# Create purchased item object
		amount = cartitem.price * cartitem.quantity
		if item.item_type() == 'usedequipment':
			commission_amount = 0 if item_handle.commission_paid else commission.commission(item)
		else:
			commission_amount = commission.commission(item)
		pi = PurchasedItem(seller=item.user,
						buyer=bu,
						order=order,
						item=item,
						unit_price=cartitem.price,
						charity = item.charity,
						charity_name = item.charity_name,
						commission = commission_amount,
						promo_code = item.promo_code,
						shipping_included=item_handle.shippingincluded,
						item_name=cartitem.item.name,
						quantity=cartitem.quantity,
						buyer_message=request.POST.get('shipping-message-'+str(cartitem.id),'')
						)
		pi.save()
		# Create notification for seller
		notification = SoldNotification(user=item.user,purchaseditem=pi)
		notification.save()
		cartitem.shoppingcart = None
		cartitem.save()
		# Update bonuses for buyer and seller, and referrer of buyer
		credits.updateCredits(bu)
		credits.updateCredits(item.user)
		if bu.referrer:
			credits.updateCredits(bu.referrer)
		# Email the seller of the item
		email_view.composeEmailItemSold_Seller(bu,pi)
		
	# 5. Mark checkout object as purchased
	checkout.purchased = True
	checkout.purchased_time = datetime.utcnow().replace(tzinfo=utc)
	checkout.save()
	
	# 6. Email confirmation
	email_view.composeEmailItemPurchased_Buyer(bu,order)
	
	return HttpResponseRedirect('/checkout/confirmation/'+str(order.id))
	
###################################
### Checkout Confirmation##########
###################################
@login_required
def checkoutConfirmation(request,orderid):
	order = Order.objects.get(id=orderid)
	if order.buyer == request.user.basicuser:
		return render_to_response('checkout/checkout_confirmation.html',{'order':order},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/cart')




#Checks if all items are available, and updates checkout accordingly
def allItemsAvailable(checkout):
	changed = False
	for cartitem in checkout.cartitem_set.all():
		if cartitem.item.liststatus != "active":
			cartitem.checkout = None
			cartitem.save()
			changed = True
		if cartitem.item.item_type() != 'usedequipment':
			if cartitem.item.item_handle().quantity < cartitem.quantity:
				checkout.cartitem.quantity = cartitem.item.item_handle().quantity
				checkout.cartitem.save()
				changed = True
	if changed:
		return 'Some items in your cart are no longer available or the quantity changed. Your cart has been updated'
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

	# Next check if it has been too long: 20 minutes to complete checkout
	time_now = datetime.utcnow().replace(tzinfo=utc)
	time_elapsed = time_now - checkout.start_time
	seconds_elapsed = time_elapsed.seconds
	if seconds_elapsed > 1200:
		dict = {'status':100,'error':'timeout'}
	
	# See if it is the right user
	if request.user.is_authenticated():
		bu = request.user.basicuser
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
