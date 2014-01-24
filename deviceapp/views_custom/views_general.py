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
import math
import difflib
import locale
import time


def index(request):
	items = Item.objects.filter(liststatus='active').order_by('savedcount')[:9]
	return render_to_response('general/index.html',{'featured':items},context_instance=RequestContext(request))

def categories(request):
	return render_to_response('general/categories.html',{'categories':Category.objects.all()},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('general/faqs.html',context_instance=RequestContext(request))

def pvp(request):
	return render_to_response('general/pvp.html',context_instance=RequestContext(request))

def about(request):
	return render_to_response('general/about.html',context_instance=RequestContext(request))

def testemail(request):
	return render_to_response('email_templates/test_email.html',context_instance=RequestContext(request))
	
def my_404_view(request):
	return render_to_response('404.html',context_instance=RequestContext(request))
	
def buyerprotect(request):
	return render_to_response('general/buyerprotect.html',context_instance=RequestContext(request))

### Anytime there is an error, send the user here ####
def error(request,errorname):
	errormessage = ''
	if errorname == 'notpost':
		errormessage = 'There was an invalid POST request'
	if errorname == 'signup':
		errormessage = 'There was an error signing up'
	if errorname == 'itemdoesnotexist':
		errormessage = 'This item has been taken down or sold'
	return render_to_response('general/error.html',{'errormessage':errormessage},context_instance=RequestContext(request))


#################################################
### Promotional Codes Functionality  ############
#################################################

PROMO_CODES = {'beta14':True,'dmg1':False,'vegeta':True}

@login_required
def addPromoCode(request,itemid):
	dict = {}
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and item.user == request.user.basicuser: 
		promocode = request.POST.get('promocode','')
		promocode = promocode.lower()
		if promocode.lower() in PROMO_CODES.keys():
			if PROMO_CODES[promocode]:
				item.promo_code = promocode
				item.save()
				dict = {'status':201,'message':promoCodeText(item.promo_code)}
			else:
				dict = {'status':400,'message':"You're too late! This code has expired! Sorry"}
		else:
			dict = {'status':500,'message':'This code does not exist'}
	else:
		dict = {'status':500,'message':'Not the owner of the item'}
	return HttpResponse(json.dumps(dict), content_type='application/json')
	
def promoCodeText(promocode):
	if promocode == 'beta14':
		return 'Sweet! You will receive 50% off VetCove commission'
	if promocode == 'vegeta':
		return 'Superb! No commission fees for you!'
	return ''
	
def calculateCommission(item):
	commission_rate = .09 #If no promo codes
	total_price = item.price
	if item.promo_code == 'beta14':
		commission_rate = .045
	if item.promo_code == 'vegeta':
		commission_rate = 0
	return int(total_price*comission_rate)

### Takes an integer and converts into dollar format #####
def convertIntPriceToDollars(int_price):
	int_price = str(int_price)
	dollars = list(int_price[0:-2])
	for i in range(len(int_price)-5,0,-3):
		dollars.insert(i,',')
	dollars = "".join(dollars)
	return "$"+dollars+'.'+int_price[-2:]
	
	
	
	
	
	
	
	
	
	
	