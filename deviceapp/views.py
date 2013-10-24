from django.shortcuts import render_to_response, redirect
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



###########################################
#### Static Pages #########################
###########################################

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))


###########################################
#### Search ###############################
###########################################	
def search(request):
	if request.method == 'GET':
		#Generate a search tree. STILL NEEDS SOME WORK 
		searchtree = {}
		requestparams = {'category':request.GET.get('category','').lower(),'industry':request.GET.get('industry','').lower()}
		if len(requestparams['industry']) and len(requestparams['category']) > 0:
			searchtree['industry'] = requestparams['industry']
			industry = Industry.objects.get(name=requestparams['industry'])
			categories = DeviceCategory.objects.filter(industries=industry)
			searchtree['category'] = categories
			searchtree['search'] = requestparams['category']+" in "+requestparams['industry']
			#Get all products that match the device category and industry if applicable
			devicecategory = DeviceCategory.objects.filter(name=requestparams['category'])
			products = Product.objects.filter(industries=industry).filter(devicecategory=devicecategory)
			searchtree['products'] = products
			
	return render_to_response('search.html',searchtree,context_instance=RequestContext(request))
	
def autosuggest(request):
	results=[]
	if request.method == 'GET':
		searchterm = request.GET['searchterm']
		categories = DeviceCategory.objects.filter(name__icontains=searchterm)
		for cat in categories:
			results.append({'type':'category','name':cat.name,'industry':"",'link':"/search?querytype=category&query="+cat.name})
			industries = cat.industries.all()
			for ind in industries:
				results.append({'type':'category','name':cat.name,'industry':" in "+ind.name.lower(),"link":"/search?querytype=category&industry="+ind.name+"&query="+cat.name});
		results = results[0:10]
		products = Product.objects.filter(name__icontains=searchterm)
		for pro in products:
			results.append({'type':'product','name':pro.name,'category':pro.devicecategory.name,'image':pro.mainimage,'link':"/product/"+str(pro.id)+"/details"});
	return HttpResponse(json.dumps(results[0:20]), mimetype='application/json')
	
def searchquery(request):
	productdict = []
	if request.method == "GET" and request.GET['querytype'] == 'product':
		try:
			dc = DeviceCategory.objects.get(name=request.GET['query'])
			products = Product.objects.filter(devicecategory=dc)
			for prod in products:
				items = Item.objects.filter(product=prod)
				lowprice = 100000000
				for item in items:
					lowprice = min(lowprice,item.price)
				productdict.append({'name':prod.name,'description':prod.description,'manufacturer':prod.manufacturer.name,'mainimage':prod.mainimage,'lowprice':lowprice})
		except ObjectDoesNotExist:
			product = none
	return HttpResponse(json.dumps(productdict), mimetype='application/json')


###########################################
#### Account Settings #####################
###########################################

@login_required
def updateprofsettings(request,field):
	print "Updating settings"
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		setUserProfileDict(field,request.POST[field],bu)
		return HttpResponseRedirect("/profile")
	else:
   		return render_to_response('index.html',{'basicuser':bu},context_instance=RequestContext(request))

@login_required
def saveditems(request):
	return render_to_response('saveditems.html',context_instance=RequestContext(request))
@login_required
def listeditems(request):
	return render_to_response('listeditems.html',context_instance=RequestContext(request))
@login_required
def accounthistory(request):
	return render_to_response('accounthistory.html',context_instance=RequestContext(request))
@login_required
def settings(request):
	return render_to_response('settings.html',context_instance=RequestContext(request))
@login_required
def profile(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		return render_to_response('profile.html',{'basicuser':bu},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def addproduct(request):
	return render_to_response('addproduct.html',context_instance=RequestContext(request))


###########################################
#### Product Pages ########################
###########################################

def productdetails(request,productid):
	product = Product.objects.get(id=int(productid))
	industry = product.devicecategory.industries.all()[0]
	return render_to_response('productdetails.html',{'product':product,'industry':industry},context_instance=RequestContext(request))

def buyingoptions(request,productid):
	product = Product.objects.get(id=int(productid))
	industry = product.devicecategory.industries.all()[0]
	sellers = Item.objects.filter(product=product)
	sellerlist = []
	for s in sellers:
		sellerimages = s.userimage_set.all()
		sellerlist.append({'seller':s,'images':sellerimages});
	return render_to_response('buyingoptions.html',{'product':product,'industry':industry,'sellers':sellerlist},context_instance=RequestContext(request))


###########################################
#### Logins and new users #################
###########################################

def loginview(request):
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
			state=state,website=website,phonenumber=phonenumber,password=password)
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
		usermodel.password = value
	usermodel.save()
	return
	