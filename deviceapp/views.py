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

import time
#If you want to test network latency
#import time
#time.sleep(5)
###########################################
#### Static Pages #########################
###########################################

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

def listintro(request):
	return render_to_response('listintro.html',context_instance=RequestContext(request))

#Save an image to S3 and send back the id of the userimage object, so when the item post is completed
#it can use the id to attach an item to the userimage object
def imageupload(request):
	imagehandlers = []
	for file in request.FILES.getlist('files'):
		ui = ItemImage(photo=file)
		ui.save()
		imagehandlers.append([ui.id,ui.photo.url])
	return HttpResponse(json.dumps(imagehandlers), mimetype='application/json')

###########################################
#### User Function Pages ##################
###########################################

def postitem(request):
	if request.method == "POST":
		print request
		if request.user.is_authenticated():
			name = request.POST['name']
			manufacturer = request.POST['manufacturer']
			manufacturer = Manufacturer.objects.get(name = manufacturer)
			category = request.POST['category']
			category = DeviceCategory.objects.get(name=category)
			serialno = request.POST['serialno']
			itempicsidlist = request.POST.getlist('pictureid[]','')
			shippingincluded = request.POST['shippingincluded']
			year = request.POST['year']
			type = request.POST['type']
			description = request.POST['productdescription']
			conditiondescription = request.POST['conditiondescription']
			price = request.POST['price']
			quality = request.POST['quality']
			contract = request.POST['contract']
			ownedlength = request.POST['ownedlength'].split("/")
			ownedlength = ownedlength[2]+"-"+ownedlength[0]+"-"+ownedlength[1]
			bu = BasicUser.objects.get(user=request.user)
			try:
				mainimage = Image.objects.get(id=request.POST['mainpicid'])
			except:
				mainimage = Image.objects.get(id=1)
			itemhandle = Item(user=bu,type=type,name=name,devicecategory=category,manufacturer=manufacturer,productdescription=description,conditiondescription=conditiondescription,year=year,contract=contract,condition=quality,price=price,dateacquired=ownedlength,liststatus="active",mainimage=mainimage,savedcount=0)
			itemhandle.save()
			for pics in itempicsidlist:
				try:
					pichandle = ItemImage.objects.get(id=pics)
					pichandle.item = itemhandle
					pichandle.save()
				except:
					pihandle = ProductImage.objects.get(id=pics)
					pihandle.item.add(pihandle)
					pihandle.save()
			return HttpResponse(json.dumps("100"), mimetype='application/json')
		else:
			return HttpResponse(json.dumps("500"), mimetype='application/json')
	return render_to_response('index.html',context_instance=RequestContext(request))

def saveitem(request):
	if request.method == "POST" and request.user.is_authenticated():
		item = Item.objects.get(id=request.POST['id'])
		print request.POST['action']
		if (request.POST['action'] == "save"):
			if not SavedItem.objects.filter(user = BasicUser.objects.get(user=request.user),item=item).exists():
				si = SavedItem(user = BasicUser.objects.get(user=request.user),item=item)
				si.save()
		else:
			if SavedItem.objects.filter(user = BasicUser.objects.get(user=request.user),item=item).exists():
				si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
				si.delete()
		return HttpResponse(json.dumps("100"), mimetype='application/json')
	else:
		return HttpResponse(json.dumps("500"), mimetype='application/json')

def removeitem(request):
	if request.method == "POST" and request.user.is_authenticated():
		item = Item.objects.get(id=request.POST['itemid'])
		si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
		si.delete()
		return HttpResponseRedirect("/saveditems")
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
	itemqs = Item.objects.filter(devicecategory=category)
	#Get price range for price slider
	for itm in itemqs:
		pricelow = min(pricelow,itm.price)	
		pricehigh = max(pricehigh,itm.price)	
	return render_to_response('search.html',{'pricelow':pricelow,'pricehigh':pricehigh,'searchquery':searchquery,'items':itemqs,'categories':catlist,'category':category,'ind':industrysearch.name,'manufacturer':manufacturers},context_instance=RequestContext(request))

def autosuggest(request):
	results=[]
	searchterm = request.GET['searchterm']
	industry = Industry.objects.get(id=1)
	#Find all categories that match the search term
	categories = DeviceCategory.objects.filter(name__icontains=searchterm)
	#Add all matched categories
	for cat in categories:
		results.append({'type':'category','name':cat.displayname,'industry':"",'link':"/productsearch/"+industry.name+"/"+cat.name})
		results = results[0:10]
	
	#Find all items that match the search term
	item = Item.objects.filter(devicecategory__name__icontains=searchterm)
	for itm in item:
		results.append({'type':'product','name':itm.name,'category':itm.user.company,'mainimage':itm.mainimage.photo.url,'link':"/item/"+str(itm.id)+"/details"});
	
	#Do a relative match if no results are found
	if len(results) == 0:
		allitems = Item.objects.all()
		itemnames = []
		matchlist = []
		for p in allitems:
			itemnames.append(str(p.name))
			if difflib.SequenceMatcher(None,searchterm,p.name.lower()).ratio() > .35:
				matchlist.append(p)
		for itm in matchlist:
			results.append({'type':'product','name':itm.name,'category':itm.user.company,'mainimage':itm.mainimage.photo.url,'link':"/item/"+str(itm.id)+"/details"});
	return HttpResponse(json.dumps(results[0:20]), mimetype='application/json')

def customsearch(request):
	if request.method == "GET":
		searchword = request.GET['q']
		allitems = Item.objects.all()
		itemnames = []
		itemqs = []
		for p in allitems:
			itemnames.append(str(p.name))
			if difflib.SequenceMatcher(None,searchword,p.name.lower()).real_quick_ratio() > .25:
				itemqs.append(p)
		pricelow = 1000000
		pricehigh = 0
		industrysearch = Industry.objects.get(id=1)
		industryterm = industrysearch.displayname
		searchquery = searchword
		catlist = DeviceCategory.objects.order_by('totalunits').reverse()
		manufacturers = Manufacturer.objects.all()
		#Get price range for price slider
		for itm in itemqs:
			pricelow = min(pricelow,itm.price)	
			pricehigh = max(pricehigh,itm.price)	
		return render_to_response('search.html',{'pricelow':pricelow,'pricehigh':pricehigh,'searchquery':searchquery,'items':itemqs,'categories':catlist,'ind':industrysearch.name,'manufacturer':manufacturers},context_instance=RequestContext(request))



	
def searchquery(request):
	itemdict = []
	if request.method == "GET":
		itemdict = []
		filters = {'pricehigh':request.GET['pricehigh'],'pricelow':request.GET['pricelow'],'new':request.GET['new'],'refurbished':request.GET['refurbished'],'preowned':request.GET['preowned']}
		try:
			dc = DeviceCategory.objects.get(name=request.GET['category'])
			items = Item.objects.filter(devicecategory=dc)
		except:
			items = Item.objects.all()
		itemspassed = []
		for item in items:
			if item.price <= int(filters['pricehigh']) and item.price >= int(filters['pricelow']):
				if (item.type == 'new' and filters['new']=='true') or (item.type == 'refurbished' and filters['refurbished']=='true') or (item.type == 'preowned' and filters['preowned']=='true'):
					itemspassed.append(item)
	html = render(request, 'productsearchitem.html', {'items':itemspassed,'resultscount':len(itemspassed)},content_type="application/html")
	return HttpResponse(html)

#Will eventually use this function later on with a product centric search view
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
		saveditems = bu.saveditem_set.all()
		saveditemcount = len(saveditems)
		listeditemcount = bu.item_set.all().count()
		items = []
		for si in saveditems:
			items.append(si.item)
		return render_to_response('saveditems.html',{"items":items,"saveditemcount":saveditemcount,"listeditemcount":listeditemcount},context_instance=RequestContext(request))
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
		return render_to_response('listeditems.html',{"items":items,"saveditemcount":saveditemcount,"listeditemcount":listeditemcount},context_instance=RequestContext(request))
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
		return render_to_response('profile.html',{'basicuser':bu,"saveditemcount":saveditemcount,"listeditemcount":listeditemcount},context_instance=RequestContext(request))
	else:
   		return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def addproduct(request):
	return render_to_response('addproduct.html',context_instance=RequestContext(request))
@login_required
def listproduct(request):
	manufacturers = Manufacturer.objects.all()
	categories = DeviceCategory.objects.all()
	return render_to_response('listproduct.html',{'manufacturers':manufacturers,'devicecategories':categories},context_instance=RequestContext(request))

@login_required
def productpreview(request,itemid):
	images = TestImage.objects.all()
	return render_to_response('addproduct2.html',{'images':images},context_instance=RequestContext(request))

###########################################
#### Product Pages ########################
###########################################

def itemdetails(request,itemid):
	item = Item.objects.get(id=int(itemid))
	industry = Industry.objects.get(id=1)
	saved = False
	if request.user.is_authenticated():
		if SavedItem.objects.filter(user = BasicUser.objects.get(user=request.user),item=item).exists():
			saved = True
	return render_to_response('productdetails.html',{'saved':saved,'item':item,'industry':industry},context_instance=RequestContext(request))

def itemoptions(request,itemid):
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
	if len(amount > 3):
		return		