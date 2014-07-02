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
from listing.models import *
from general.forms import *


#############################################################
######## General Pages ######################################
#############################################################

### Manually view the browser upgrade page
def browserUpgrade(request):
	return render_to_response('general/ieupgrade.html',{},context_instance=RequestContext(request))

### Homepage ####
def index(request):
	# If the user is authenticated, show the appropriate homepage
	if request.user.is_authenticated():
		return HttpResponseRedirect('/dashboard')
	# If the user is not logged in, render the generic page
	else:
		return render_to_response('general/index.html',{},context_instance=RequestContext(request))

### Category Directory ###
def categories(request):
	categories = Category.objects.all().prefetch_related('parent').order_by('displayname')
	maincategories = categories.filter(main=True).order_by('displayname')
	for maincat in maincategories:
	 	maincat.subcategories = [subcat for subcat in categories if subcat.parent == maincat]
	return render_to_response('general/categories.html',{'pagecategories':maincategories},context_instance=RequestContext(request))

### Referral Landing Page ###
def newReferral(request,referral_id):
	request.session['referral_id'] = referral_id
	return render_to_response('general/index.html',{},context_instance=RequestContext(request))

#############################################################
######## Corporate Pages ####################################
#############################################################

### Features for Veterinarians ###
def features(request):
	return render_to_response('general/corporate/features.html',{},context_instance=RequestContext(request))

### Features for Manufacturer ###
def manufacturer(request):
	return render_to_response('general/corporate/manufacturer.html',{},context_instance=RequestContext(request))

### Features for Distributor ###
def supplier(request):
	return render_to_response('general/corporate/supplier.html',{},context_instance=RequestContext(request))

#############################################################
######## Information Pages ##################################
#############################################################

def tos(request):
	return render_to_response('general/information/tos.html',{'tos':True},context_instance=RequestContext(request))

def giveback(request):
	return render_to_response('general/information/giveback.html',{'giveback':True},context_instance=RequestContext(request))

def pricing(request):
	return render_to_response('general/information/pricing.html',{'pricing':True},context_instance=RequestContext(request))

def rewards(request):
	return render_to_response('general/information/rewards.html',{'rewards':True},context_instance=RequestContext(request))

def privacypolicy(request):
	return render_to_response('general/information/privacypolicy.html',{'privacypolicy':True},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('general/information/faqs.html',{'faq':True},context_instance=RequestContext(request))

def about(request):
	return render_to_response('general/information/about.html',{'about':True},context_instance=RequestContext(request))

def buyerprotect(request):
	return render_to_response('general/information/buyerprotect.html',{'buyerprotect':True,'PHONE_NUMBER':settings.CONTACT_PHONE_NUMBER},context_instance=RequestContext(request))

#############################################################
######## Contact ############################################
#############################################################

def contact(request):
	return render_to_response('general/information/contact.html',{'contact':True},context_instance=RequestContext(request))

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

#############################################################
######## Error Pages ########################################
#############################################################

def my_404_view(request):
	return render_to_response('404.html',context_instance=RequestContext(request))

def my_500_view(request):
	return render_to_response('500.html',context_instance=RequestContext(request))

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

	
	