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


def cart(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		shoppingcart = ShoppingCart.objects.get(user=bu)
	else:
		if 'shoppingcart' in request.session:
			shoppingcart = ShoppingCart.objects.get(id=request.session['shoppingcart'])
		else:
			shoppingcart = None
	if shoppingcart:
		count = 0
		totalcost = 0
		for cartitem in shoppingcart.cartitem_set.all():
			count += cartitem.quantity
			totalcost += cartitem.quantity * cartitem.item.price
	dict = {'shoppingcart':shoppingcart,'total':totalcost,'itemcount':count}
	return render_to_response('account/cart.html',dict,context_instance=RequestContext(request))

def addToCart(request,itemid):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		shoppingcart = ShoppingCart.objects.get(user=bu)
	else:
		if 'shoppingcart' in request.session:
			shoppingcart = ShoppingCart.objects.get(id=request.session['shoppingcart'])
		else:
			shoppingcart = ShoppingCart()
			shoppingcart.save()
			request.session['shoppingcart'] = shoppingcart.id
	item = Item.objects.get(id=itemid)
	newCartItem, created = CartItem.objects.get_or_create(shoppingcart=shoppingcart,item=item,quantity=1)
	newCartItem.save()
	return HttpResponseRedirect('/cart')
		
	
def updatecart(request):
	item = Item.objects.get(id=request.POST.get('itemid',''))
	method = request.POST.get('method','')
	quantity = request.POST.get('quantity','')
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		shoppingcart = ShoppingCart.objects.get(user=bu)
	#Anonymous shopping cart
	else:
		#Get shopping cart from shopping cart id, otherwise create new one and set cookie
		shoppingcartid = int(request.session['shoppingcart'])
		shoppingcart = ShoppingCart.objects.get(id=shoppingcartid)
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
		
	#Get the total number of items and total cost
	count = 0
	totalcost = 0
	for cartitem in shoppingcart.cartitem_set.all():
		count += cartitem.quantity
		totalcost += cartitem.quantity * cartitem.item.price
	dict = {'status':400,'total':"$"+"{:,}".format(totalcost),'count':count}
	return HttpResponse(json.dumps(dict), content_type='application/json')
		
		
	
def checkoutSignin(request,itemid):
	return render_to_response('checkout/checkout_login.html',{},context_instance=RequestContext(request))

def checkoutShipping(request,itemid):
	return render_to_response('checkout/checkout_shipping.html',{},context_instance=RequestContext(request))

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
###### Checkout Login Methods #####################
####################################################

def checkoutlogin(request,itemid):
	user = authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			bu = BasicUser.objects.get(user=request.user)
			item = Item.objects.get(id=itemid)
			checkout = Checkout(item=item,buyer=bu,shipping_address=None,payment=None,state='login')
			checkout.save()
			return HttpResponseRedirect('/checkout/payment/'+checkout.id)
		else:
			return HttpResponse("Your account has been disabled")
	else:
		return render_to_response('checkout/checkout_login.html',{'outcome':'Invalid Login'},context_instance=RequestContext(request))

	return HttpResponse('hre')

