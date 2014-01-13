from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.timezone import utc
import json
import math
import difflib
import locale
import time
from datetime import datetime


###########################################
#### Logins and new users #################
###########################################

def loginview(request):
	next = request.GET.get('next',None)
	action = request.GET.get('action',None)
	return render_to_response('account/login.html',{'next':next,'action':action},context_instance=RequestContext(request))

def lgnrequest(request):
	username = request.POST['email']
	password = request.POST['password']
	user = authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			if 'shoppingcart' in request.session:
				bu = BasicUser.objects.get(user=user)
				user_shoppingcart = ShoppingCart.objects.get(user=bu)
				session_shoppingcart = ShoppingCart.objects.get(id=request.session['shoppingcart'])
				for cartitems in session_shoppingcart.cartitem_set.all():
					if not CartItem.objects.filter(item=cartitems.item,shoppingcart=user_shoppingcart).exists():			
						ci = CartItem(item=cartitems.item,shoppingcart=user_shoppingcart,quantity=1)
						ci.save()
			login(request,user)
			try:
				request.GET['next']
				return HttpResponseRedirect(request.GET['next'])
			except:
				return HttpResponseRedirect("/signup")
		else:
			return HttpResponse("Your account has been disabled")
	else:
		return render_to_response('account/login.html',{'outcome':'Invalid Login'},context_instance=RequestContext(request))

def signup(request):
	if request.method == 'GET':
		error = request.GET.get('e','')
	if request.user.is_authenticated():
		return HttpResponseRedirect("/account/profile")
	return render_to_response('account/signup.html',{'error':error},context_instance=RequestContext(request))

def checkemail(request):
	if request.method == "GET":
		email = request.GET['email']
		if User.objects.filter(username=email).count():
			return HttpResponse(json.dumps('invalid'), content_type='application/json')
		else:
			return HttpResponse(json.dumps('valid'), content_type='application/json')
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
def updateprofsettings(request,field):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		if field == 'password':
			change = setUserProfileDict(field,[request.POST['password1'],request.POST['password2']],bu)
			if change != 'Success':
				return HttpResponseRedirect("/account/profile?e=password")
		else:
			change = setUserProfileDict(field,request.POST[field],bu)
		return HttpResponseRedirect("/account/profile")
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def wishlist(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		saveditems = bu.saveditem_set.all()
		items = []
        	for si in saveditems:
        		items.append(si.item)
		return render_to_response('account/buying/wishlist.html',{"wishlist":True,"items":items},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))
   		
@login_required
def listings(request,listingtype):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		if listingtype != 'all':
			listeditems = bu.item_set.all().filter(liststatus=listingtype)
		else:
			listeditems = bu.item_set.all()
		return render_to_response('account/selling/listeditems.html',{"listpage":True,"items":listeditems, "listingtype":listingtype},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html', context_instance=RequestContext(request))
 
@login_required
def buyhistory(request):
	if request.user.is_authenticated():
		return render_to_response('account/buying/buyhistory.html',{},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def sellhistory(request):
	if request.user.is_authenticated():
		return render_to_response('account/selling/sellhistory.html',{},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def usersettings(request):
	if request.user.is_authenticated():
		return render_to_response('account/settings.html',{},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def profile(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		dict = {'basicuser':bu}
		if request.method == "GET":
			if request.GET.get('e','') == 'password':
				dict['error']= "Password"
		return render_to_response('account/profile.html',dict,context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def payment(request):
	return render_to_response('account/payment.html',{'payment':True},context_instance=RequestContext(request))
	
@login_required
def sellerquestions(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)	
		questions = Question.objects.filter(seller=bu)
		answered = []
		unanswered = []
		for question in questions:
			if question.answer:
				answered.append(question)
			else:
				unanswered.append(question)
		return render_to_response('account/questions/sellerquestions.html',{'answered':answered,'unanswered':unanswered},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

@login_required
def buyerquestions(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)	
		questions = Question.objects.filter(buyer=bu)
		return render_to_response('account/questions/buyerquestions.html',{'questions':questions},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))
 
@login_required
def answerquestion(request,questionid):
	if request.user.is_authenticated() and request.method == "POST":
		bu = BasicUser.objects.get(user=request.user)
		question = Question.objects.get(id=questionid)
		if question.item.user.id == bu.id:
			question.answer = request.POST.get('answer','')
			question.dateanswered = datetime.utcnow().replace(tzinfo=utc)
			question.save()
		return HttpResponseRedirect('/account/sellerquestions')
	return HttpResponseRedirect('/')
 	  		
#################################################
### Helper function to update a user's profile  #
#################################################

def setUserProfileDict(field,value,usermodel):
	if field == 'businesstype':
		usermodel.businesstype = value
	elif field == 'company':
		usermodel.company = value
	elif field == 'name':
		usermodel.name = value
	elif field == 'address':
		usermodel.address = value
	elif field == 'email':
		usermodel.email = value
	elif field == 'city':
		usermodel.city = value
	elif field == 'state':
		usermodel.state = value
	elif field == 'zipcode':
		usermodel.zipcode = value
	elif field == 'phonenumber':
		usermodel.phonenumber = value
	elif field == 'password':
		if usermodel.user.check_password(value[0]):
			usermodel.user.set_password(value[1])
			usermodel.user.save()
		else:
			return "Error"
	usermodel.save()
	return "Success"