from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.conf import settings
import json, math, difflib, locale, time, string
from django.core.cache import cache
from general.models import *
from listing.models import Item, Category, SubCategory
from general.forms import *
from helper import commission as commission

def product(request,itemid):
	return render_to_response('product/product2.html',{},context_instance=RequestContext(request))

def features(request):
	return render_to_response('general/features.html',{},context_instance=RequestContext(request))

def manufacturer(request):
	return render_to_response('general/manufacturer.html',{},context_instance=RequestContext(request))

def trending(request):
	return render_to_response('general/trending.html',{},context_instance=RequestContext(request))

def index(request):
	return render_to_response('general/index.html',{},context_instance=RequestContext(request))

def sell(request):
	return render_to_response('general/sell.html',{},context_instance=RequestContext(request))

def buy(request):
	return render_to_response('general/buy.html',{},context_instance=RequestContext(request))

def shop(request):
	return render_to_response('search/shop.html',{},context_instance=RequestContext(request))

def tos(request):
	return render_to_response('general/tos.html',{'tos':True},context_instance=RequestContext(request))

def giveback(request):
	return render_to_response('general/giveback.html',{'giveback':True},context_instance=RequestContext(request))

def pricing(request):
	return render_to_response('general/pricing.html',{'pricing':True},context_instance=RequestContext(request))

def privacypolicy(request):
	return render_to_response('general/privacypolicy.html',{'privacypolicy':True},context_instance=RequestContext(request))

def categories(request):
	categories = Category.objects.all().prefetch_related('subcategory_set')
	for cat in categories:
		subcategories = cat.subcategory_set.all().order_by('displayname')
		length = math.ceil(len(subcategories)/3.0)
		cat_array = [[],[],[]]
		for i in range(len(subcategories)):
			row = int(math.floor((i)/length))
			cat_array[row].append(subcategories[i])
		cat.subcat = cat_array
	return render_to_response('general/categories.html',{'categories':categories},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('general/faqs.html',{'faq':True},context_instance=RequestContext(request))

def pvp(request):
	return render_to_response('general/pvp.html',{'pvp':True},context_instance=RequestContext(request))

def about(request):
	return render_to_response('general/about.html',{'about':True},context_instance=RequestContext(request))

def my_404_view(request):
	return render_to_response('404.html',context_instance=RequestContext(request))

def my_500_view(request):
	return render_to_response('500.html',context_instance=RequestContext(request))
	
def buyerprotect(request):
	return render_to_response('general/buyerprotect.html',{'buyerprotect':True,'PHONE_NUMBER':settings.CONTACT_PHONE_NUMBER},context_instance=RequestContext(request))

def contact(request):
	return render_to_response('general/contact.html',{'contact':True},context_instance=RequestContext(request))

def newReferral(request,referral_id):
	request.session['referral_id'] = referral_id
	return render_to_response('general/referral.html',{},context_instance=RequestContext(request))

#Intro Page
def listintro(request):
	category = Category.objects.all().extra(order_by = ['displayname'])
	return render_to_response('product/listintro.html',{'categories':category},context_instance=RequestContext(request))

def contactform(request):
	form = ContactForm(request.POST)
	if form.is_valid():		
		# General user sign-up
		name = form.cleaned_data['name']
		email = form.cleaned_data['email']
		message = form.cleaned_data['message']
		user = None
		if request.user.is_authenticated():
			user = request.user.basicuser
		cf = Contact(user=user,name=name,email=email,message=message)
		cf.save()
		email_view.composeContactForm(cf)
		return render_to_response('general/contact.html',{'contact':True,'success':True},context_instance=RequestContext(request))	
	return render_to_response('general/contact.html',{'contact':True,'failure':True},context_instance=RequestContext(request))

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

	
	
	
	