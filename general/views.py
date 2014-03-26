from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.conf import settings
import json, math, difflib, locale, time
from django.core.cache import cache
from general.models import *
from listing.models import Item, Category
from general.forms import *
from helper import commission as commission

def index(request):
	items = Item.objects.filter(liststatus='active').filter(subcategory__category__type='equipment').order_by('savedcount')[:24]
	return render_to_response('responsive/general/index.html',{'featured':items},context_instance=RequestContext(request))

def sell(request):
	return render_to_response('responsive/general/sell.html',{},context_instance=RequestContext(request))

def portalSeller(request):
	return render_to_response('portal/base.html',{'seller_portal':True},context_instance=RequestContext(request))

def portalBuyer(request):
	return render_to_response('responsive/genereal/buy.html',{'buyer_portal':True},context_instance=RequestContext(request))

def portalLogin(request):
	return render_to_response('portal/login.html',{},context_instance=RequestContext(request))

def portal_analytics(request):
	return render_to_response('portal/analytics.html',{'analytics':True},context_instance=RequestContext(request))

def portal_listing(request):
	return render_to_response('portal/listing.html',{'listing':True},context_instance=RequestContext(request))

def portal_solditems(request):
	return render_to_response('portal/solditems.html',{'solditems':True},context_instance=RequestContext(request))

def portal_account(request):
	return render_to_response('portal/account.html',{'account':True},context_instance=RequestContext(request))

def buy(request):
	return render_to_response('responsive/general/buy.html',{},context_instance=RequestContext(request))

def shop(request):
	return render_to_response('search/shop.html',{},context_instance=RequestContext(request))

def tos(request):
	return render_to_response('responsive/general/tos.html',{'tos':True},context_instance=RequestContext(request))

def giveback(request):
	return render_to_response('responsive/general/giveback.html',{'giveback':True},context_instance=RequestContext(request))

def commissionpage(request):
	return render_to_response('responsive/general/commission.html',{'commission':True},context_instance=RequestContext(request))

def privacypolicy(request):
	return render_to_response('responsive/general/privacypolicy.html',{'privacypolicy':True},context_instance=RequestContext(request))

def equipmentcategories(request):
	categories = Category.objects.all().filter(type='equipment').order_by('name')
	return render_to_response('general/equipmentcategories.html',{'categories':categories},context_instance=RequestContext(request))

def pharmacategories(request):
	categories = Category.objects.all().filter(type='pharma').order_by('name')
	return render_to_response('general/pharmacategories.html',{'categories':categories},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('responsive/info/faq.html',{'faq':True},context_instance=RequestContext(request))

def pvp(request):
	return render_to_response('responsive/general/pvp.html',{'pvp':True},context_instance=RequestContext(request))

def about(request):
	return render_to_response('responsive/general/about.html',{'about':True},context_instance=RequestContext(request))

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

	
	
	
	