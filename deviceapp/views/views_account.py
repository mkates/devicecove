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
import json
import math
import difflib
import locale
import time


###########################################
#### Logins and new users #################
###########################################

def loginview(request):
	print 'started'
	try:
		next = request.GET['next']
	except:
		next = None
	return render_to_response('login.html',{'next':next},context_instance=RequestContext(request))

def lgnrequest(request):
	username = request.POST['email']
	password = request.POST['password']
	user = authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			try:
				request.GET['next']
				return HttpResponseRedirect(request.GET['next'])
			except:
				return HttpResponseRedirect("/signup")
		else:
			return HttpResponse("Your account has been disabled")
	else:
		return render_to_response('login.html',{'outcome':'Invalid Login'},context_instance=RequestContext(request))

def signup(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/profile")
	return render_to_response('signup.html',context_instance=RequestContext(request))
	
def newuserform(request):
	if request.method == 'POST':
		try:
			businesstype = request.POST['businesstype']
			company = request.POST['company']
			name = request.POST['name']
			email = request.POST['email']
			address = request.POST['address']
			zipcode = request.POST['zipcode']
			city = request.POST['city']
			state = request.POST['state']
			website = request.POST['website']
			phonenumber = request.POST['phonenumber']
			password = request.POST['password']
			newuser = User.objects.create_user(email,email,password)
			newuser.save()
			nbu = BasicUser(user=newuser,name=name,businesstype=businesstype,company=company,email=email,address=address,zipcode=zipcode,city=city,
			state=state,website=website,phonenumber=phonenumber)
			nbu.save()
			user = authenticate(username=newuser,password=password)
			login(request,user)
			return render_to_response('index.html',context_instance=RequestContext(request))
		except Exception,e:
			return HttpResponse(e)
	return HttpResponse("Not a POST method?")
	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def forgotpassword(request):
	return render_to_response('passwordreset.html',context_instance=RequestContext(request))

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
				return HttpResponseRedirect("/profile?e=password")
		return HttpResponseRedirect("/profile")
	else:
   		return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def saveditems(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		saveditems = bu.saveditem_set.all()
		saveditemcount = len(saveditems)
		listeditemcount = bu.item_set.all().count()
		items = []
		for si in saveditems:
			items.append(si.item)
		return render_to_response('saveditems.html',{"savedpage":True,"items":items,"saveditemcount":saveditemcount,"listeditemcount":listeditemcount},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html', context_instance=RequestContext(request))
   		
@login_required
def listeditems(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		listeditems = bu.item_set.all()
		listeditemcount = len(listeditems)
		saveditemcount = bu.saveditem_set.all().count()
		items = bu.item_set.all()
		return render_to_response('listeditems.html',{"listpage":True,"items":items,"saveditemcount":saveditemcount,"listeditemcount":listeditemcount},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html', context_instance=RequestContext(request))
 
@login_required
def accounthistory(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		listeditemcount = bu.item_set.all().count()
		saveditemcount = bu.saveditem_set.all().count()
		return render_to_response('accounthistory.html',{"saveditemcount":saveditemcount,"listeditemcount":listeditemcount},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def settings(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		listeditemcount = bu.item_set.all().count()
		saveditemcount = bu.saveditem_set.all().count()
		return render_to_response('settings.html',{"saveditemcount":saveditemcount,"listeditemcount":listeditemcount},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def profile(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		listeditemcount = bu.item_set.all().count()
		saveditemcount = bu.saveditem_set.all().count()
		dict = {'basicuser':bu,"saveditemcount":saveditemcount,"listeditemcount":listeditemcount}
		if request.method == "GET":
			try:
				error = request.GET['e']
				if error == 'password':
					dict['error']= "Password"
			except:
				print 'error code wrong'
		return render_to_response('profile.html',dict,context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def addproduct(request):
	return render_to_response('addproduct.html',context_instance=RequestContext(request))

@login_required
def listproduct(request):
	if request.method == "GET":
		manufacturers = Manufacturer.objects.all()
		categories = DeviceCategory.objects.all()
		dict = {'manufacturers':manufacturers,'devicecategories':categories}
		manufacturer = Manufacturer.objects.get(name=request.GET['manufacturer'])
		devicecategory = DeviceCategory.objects.get(name=request.GET['category'])
		dict['model'] = request.GET['name']
		name = request.GET['name']
		try:
			product = Product.objects.get(name=name)
			dict['product'] = product
		except:
			system_match = False
		for mans in manufacturers:
			if manufacturer.name == mans.name:
				mans.active = True
		for cats in categories:
			if devicecategory.name == cats.name:
				cats.active = True
	return render_to_response('listproduct.html',dict,context_instance=RequestContext(request))

@login_required
def edititem(request,itemid):
	item = Item.objects.get(id=itemid)
	images = item.itemimage_set.all()
	imageids = []
	for img in images:
		imageids.append(img.id)
	item.imageids = imageids
	manufacturers = Manufacturer.objects.all()
	for mans in manufacturers:
		if item.manufacturer == mans:
			mans.active = True
	categories = DeviceCategory.objects.all()
	for cats in categories:
		if item.devicecategory == cats:
			cats.active = True
	return render_to_response('editlisting.html',{'manufacturers':manufacturers,'devicecategories':categories,'editing':True,'item':item},context_instance=RequestContext(request))

			
@login_required
def productpreview(request,itemid):
	images = TestImage.objects.all()
	return render_to_response('addproduct2.html',{'images':images},context_instance=RequestContext(request))
	
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