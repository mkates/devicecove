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
import locale


#If you want to test network latency
#import time
#time.sleep(5)
###########################################
#### Static Pages #########################
###########################################

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

#Save an image to S3 and send back the id of the userimage object, so when the item post is completed
#it can use the id to attach an item to the userimage object
def imageupload(request):
	imagehandlers = []
	for file in request.FILES.getlist('files'):
		ui = UserImage(photo=file)
		ui.save()
		imagehandlers.append([ui.id,ui.photo.url])
	return HttpResponse(json.dumps(imagehandlers), mimetype='application/json')

###########################################
#### User Function Pages ##################
###########################################

def postitem(request):
	if request.method == "POST":
		if request.user.is_authenticated():
			productid = request.POST['productid']
			try:
				pictureidlist = request.POST['pictureid[]']
			except:
				pictureidlist = []
			description = request.POST['description']
			price = request.POST['price']
			quality = request.POST['quality']
			bu = BasicUser.objects.get(user=request.user)
			product = Product.objects.get(id=productid)
			itemhandle = Item(product=product,condition=quality,status=2,savedcount=0,user=bu,description=description, price=price,picturearray=pictureidlist)
			itemhandle.save()
			for picid in pictureidlist:
				pichandle = UserImage.objects.get(id=picid)
				pichandle.item = itemhandle
				pichandle.save()
			return HttpResponse(json.dumps("100"), mimetype='application/json')
		else:
			return HttpResponse(json.dumps("500"), mimetype='application/json')
	return render_to_response('index.html',context_instance=RequestContext(request))

def saveitem(request):
	if request.method == "POST" and request.user.is_authenticated():
		item = Item.objects.get(id=request.POST['id'])
		if (request.POST['action'] == "save"):
			try:
				si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
			except:
				si = SavedItem(user = BasicUser.objects.get(user=request.user),item=item)
				si.save()
		else:
			try:
				si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
				si.delete()
			except:
				print 'Product already exists'
		return HttpResponse(json.dumps("100"), mimetype='application/json')
	else:
		return HttpResponse(json.dumps("500"), mimetype='application/json')

def removeitem(request):
	if request.method == "POST" and request.user.is_authenticated():
		item = Item.objects.get(id=request.POST['productid'])
		si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
		si.delete()
		return HttpResponseRedirect("/profile")
	return render_to_response('index.html',context_instance=RequestContext(request))
		
###########################################
#### Search ###############################
###########################################	
def productsearch(request,industryterm,devicecategoryterm):
	catlist = DeviceCategory.objects.order_by('totalunits').reverse()
	manufacturers = Manufacturer.objects.all()
	category = DeviceCategory.objects.get(name=devicecategoryterm)
	pricelow = 1000000
	pricehigh = 0
	industrysearch = Industry.objects.get(name=industryterm)
	industryterm = industrysearch.displayname
	searchquery = category.displayname+" in "+industryterm
	categorysearch = catlist
	products = Product.objects.filter(industries=industrysearch).filter(devicecategory=category)
	for pro in products:
		for items in pro.item_set.all():
			pricelow = min(pricelow,items.price)	
			pricehigh = max(pricehigh,items.price)	
	# Parse product specifications	
	for p in range(len(products)):
		specs = products[p].specs.split(";")
		for i in range(len(specs)):
			specs[i] = specs[i].split("!")
		products[p].specifications = specs
		products[p].sellers = products[p].item_set.all();
	return render_to_response('search.html',{'pricelow':pricelow,'pricehigh':pricehigh,'searchquery':searchquery,'products':products,'categories':catlist,'category':category,'ind':industrysearch.name,'manufacturer':manufacturers},context_instance=RequestContext(request))

def autosuggest(request):
	results=[]
	searchterm = request.GET['searchterm']
	industry = Industry.objects.get(id=1)
	#Find all categories that match the search term
	categories = DeviceCategory.objects.filter(name__icontains=searchterm)
	for cat in categories:
		results.append({'type':'category','name':cat.displayname,'industry':"",'link':"/productsearch/"+industry.name+"/"+cat.name})
		results = results[0:10]
	
	#Find all products that match the search term
	products = Product.objects.filter(name__icontains=searchterm)
	for pro in products:
		results.append({'type':'product','name':pro.name,'category':pro.devicecategory.displayname,'image':pro.mainimage,'link':"/product/"+str(pro.id)+"/details"});
	
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
			results.append({'type':'product','name':pro.name,'category':pro.devicecategory.displayname,'image':pro.mainimage,'link':"/product/"+str(pro.id)+"/details"});	
	return HttpResponse(json.dumps(results[0:20]), mimetype='application/json')
	
def searchquery(request):
	productdict = []
	if request.method == "GET":
		productdict = []
		filters = {'pricehigh':request.GET['pricehigh'],'pricelow':request.GET['pricelow'],'new':request.GET['new'],'refurbished':request.GET['refurbished'],'preowned':request.GET['preowned']}
		dc = DeviceCategory.objects.get(name=request.GET['category'],)
		products = Product.objects.filter(devicecategory=dc)
		for prod in products:
			itemqs = prod.item_set.all()
			#Convert the query set into a list
			items = []
			for qs in itemqs:
				items.append(qs)
			itemspassed = []
			for i in range(len(items)):
				if items[i].price < int(filters['pricehigh']) and items[i].price > int(filters['pricelow']):
					if (items[i].type == 'new' and filters['new']=='true') or (items[i].type == 'refurbished' and filters['refurbished']=='true') or (items[i].type == 'preowned' and filters['preowned']=='true'):
						itemspassed.append(items[i])
			#If an item passes all test, then generate its product
			if len(itemspassed) > 0:
				productdict.append(getProductElementsFromItems(itemspassed,prod));	
	html = render(request, 'productsearchitem.html', {'products':productdict},content_type="application/html")
	return HttpResponse(html)

def getProductElementsFromItems(items,prod):
	specs = prod.specs.split(";")
	for i in range(len(specs)):
		specs[i] = specs[i].split("!")
	prod.specifications = specs
	lowprice = 10000000
	number_products = 0
	for item in items:
		lowprice = min(lowprice,item.price)
	return {'product':prod,'items':items,'lowprice':lowprice}
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
   		return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def saveditems(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		items = bu.saveditem_set.all()
		for item in items:
			pictures = UserImage.objects.filter(item=item)
			item.pictures = pictures
		return render_to_response('saveditems.html',{"items":items},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html', context_instance=RequestContext(request))
   		
@login_required
def listeditems(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		items = bu.item_set.all()
		for item in items:
			pictures = UserImage.objects.filter(item=item)
			item.pictures = pictures
		return render_to_response('listeditems.html',{"items":items},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html', context_instance=RequestContext(request))
   		
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
	specs = product.specs.split(";")
	for i in range(len(specs)):
		specs[i] = specs[i].split("!")
	return render_to_response('productdetails.html',{'product':product,'industry':industry,'specs':specs},context_instance=RequestContext(request))

def buyingoptions(request,productid):
	product = Product.objects.get(id=int(productid))
	industry = product.devicecategory.industries.all()[0]
	sellers = Item.objects.filter(product=product)
	for s in sellers:
		pictures = UserImage.objects.filter(item=s)
		s.pictures = pictures
		try:
			si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=s)
			s.saved = True
		except:
			s.saved = False	
	for s in sellers:
		print s.saved	
	return render_to_response('buyingoptions.html',{'product':product,'industry':industry,'sellers':sellers},context_instance=RequestContext(request))


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

def numberToMoney(amount):
	amount = str(int(amount))
	return amount
			