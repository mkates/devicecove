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
import difflib

###########################################
#### Static Pages #########################
###########################################

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

def imageupload(request):
	imagehandlers = []
	for file in request.FILES.getlist('files'):
		it = TestImage(name="testname",photo=file,thumbnail=file)
		it.save()
		print it.id
		imagehandlers.append([it.id,it.photo.url])
	return HttpResponse(json.dumps(imagehandlers), mimetype='application/json')
	
def imageformsubmit(request):
	username = request.form["username"]
	full_name = request.form["full_name"]
	avatar_url = request.form["avatar_url"]
	print avatar_url
	return render_to_response('index.html',context_instance=RequestContext(request))

###########################################
#### Search ###############################
###########################################	
def search(request):
	searchvalue = request.GET.get('q','')
	tree = Industry.objects.all()
	allproducts = Product.objects.all()
	products = []
	for p in allproducts:
		print difflib.SequenceMatcher(None,searchvalue.lower(),p.name.lower()).ratio()
		if difflib.SequenceMatcher(None,searchvalue.lower(),p.name.lower()).ratio() > .4 or len(searchvalue) == 0:
			products.append(p)
	return render_to_response('search.html',{'products':products,'tree':tree},context_instance=RequestContext(request))

def productsearch(request,industryterm,devicecategoryterm):
	industry = {}
	catlist = DeviceCategory.objects.order_by('totalunits').reverse()
	manufacturers = Manufacturer.objects.all()
	pricelow = 1000000
	pricehigh = 0
	if (industryterm == "all"):
		industrysearch = Industry.objects.all()
		searchquery = ""
	else:
		industrysearch = Industry.objects.get(name=industryterm)
		searchquery = " in "+industryterm
	if (devicecategoryterm == "all"):
		searchquery = "all products"+searchquery
		categorysearch = catlist
		products = Product.objects.filter(industries=industrysearch)
	else:
		searchquery = devicecategoryterm+searchquery
		categorysearch = DeviceCategory.objects.get(name=devicecategoryterm)
		products = Product.objects.filter(industries=industrysearch).filter(devicecategory=categorysearch)
	for pro in products:
		for items in pro.item_set.all():
			pricelow = min(pricelow,items.price)	
			pricehigh = max(pricehigh,items.price)		
			
	return render_to_response('search.html',{'pricelow':pricelow,'pricehigh':pricehigh,'searchquery':searchquery,'products':products,'categories':catlist,'ind':industryterm,'manufacturer':manufacturers},context_instance=RequestContext(request))

def autosuggest(request):
	results=[]
	searchterm = request.GET['searchterm']
	#Find all categories that match the search term
	categories = DeviceCategory.objects.filter(name__icontains=searchterm)
	for cat in categories:
		results.append({'type':'category','name':cat.name,'industry':"",'link':"/productsearch/all/"+cat.name})
		industries = cat.industries.all()
		for ind in industries:
			results.append({'type':'category','name':cat.name,'industry':" in "+ind.name.lower(),"link":"/productsearch/"+ind.name+"/"+cat.name});
	results = results[0:10]
	
	#Find all products that match the search term
	products = Product.objects.filter(name__icontains=searchterm)
	for pro in products:
		results.append({'type':'product','name':pro.name,'category':pro.devicecategory.name,'image':pro.mainimage,'link':"/product/"+str(pro.id)+"/details"});
	
	#Do a relative match if no results are found
	if len(results) == 0:
		print 'here'
		allproducts = Product.objects.all()
		productnames = []
		matchlist = []
		for p in allproducts:
			productnames.append(str(p.name))
			if difflib.SequenceMatcher(None,searchterm,p.name.lower()).ratio() > .35:
				matchlist.append(p)
		for pro in matchlist:
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

@login_required
def productpreview(request,itemid):
	images = TestImage.objects.all()
	return render_to_response('addproduct2.html',{'images':images},context_instance=RequestContext(request))

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
	