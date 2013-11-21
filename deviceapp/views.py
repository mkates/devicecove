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

#If you want to test network latency
#import time
#time.sleep(5)
###########################################
#### Static Pages #########################
###########################################


def listintro(request):
	manufacturer = Manufacturer.objects.all()
	category = DeviceCategory.objects.all().extra(order_by = ['displayname'])
	return render_to_response('listintro.html',{'manufacturer':manufacturer,'category':category},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('faqs.html',context_instance=RequestContext(request))

def buyerprotect(request):
	return render_to_response('buyerprotect.html',context_instance=RequestContext(request))
	
#Save an image to S3 and send back the id of the userimage object, so when the item post is completed
#it can use the id to attach an item to the userimage object
def imageupload(request):
	imagehandlers = []
	for file in request.FILES.getlist('files'):
		ui = ItemImage(photo=file,photo_small=file,photo_medium=file)
		ui.save()
		imagehandlers.append([ui.id,ui.photo_small.url])
	return HttpResponse(json.dumps(imagehandlers), mimetype='application/json')

###########################################
#### User Function Pages ##################
###########################################

def postitem(request):
	if request.method == "POST":
		if request.user.is_authenticated():
			name = request.POST['name']
			manufacturer = request.POST['manufacturer']
			manufacturer = Manufacturer.objects.get(name = manufacturer)
			category = request.POST['category']
			category = DeviceCategory.objects.get(name=category)
			serialno = request.POST['serialno']
			try:
				itempicsidlist = request.POST.getlist('pictureid[]','')
			except:
				itempicsidlist = []
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
				mainimage = Image.objects.get(id=request.POST['mainimageid'])
			except:
				mainimage = None
			itemhandle = Item(user=bu,type=type,name=name,devicecategory=category,shippingincluded=shippingincluded,manufacturer=manufacturer,productdescription=description,conditiondescription=conditiondescription,serialno=serialno,year=year,contract=contract,condition=quality,price=price,dateacquired=ownedlength,liststatus="active",mainimage=mainimage,savedcount=0,verified=False)
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

@login_required
def editform(request):
	if request.user.is_authenticated() and request.method == "POST":
		bu = BasicUser.objects.get(user=request.user)
		item = Item.objects.get(id=request.POST['id'])
		if item.user == bu:
			item.name = request.POST['name']
			manufacturer = request.POST['manufacturer']
			item.manufacturer = Manufacturer.objects.get(name = manufacturer)
			category = request.POST['category']
			item.devicecategory = DeviceCategory.objects.get(name=category)
			item.serialno = request.POST['serialno']
			try:
				itempicsidlist = request.POST.getlist('pictureid[]','')
			except:
				itempicsidlist = []
			item.shippingincluded = request.POST['shippingincluded']
			item.year = request.POST['year']
			item.type = request.POST['type']
			item.productdescription = request.POST['productdescription']
			item.conditiondescription = request.POST['conditiondescription']
			item.price = request.POST['price']
			if int(request.POST['mainimageid']) != -1:
				item.mainimage = Image.objects.get(id=request.POST['mainimageid'])
			else:
				item.mainimage = None
			item.quality = request.POST['quality']
			item.contract = request.POST['contract']
			ownedlength = request.POST['ownedlength'].split("/")
			item.dateacquired = ownedlength[2]+"-"+ownedlength[0]+"-"+ownedlength[1]
			#Delete item pictures they remove
			oldPictureIdhandle = item.itemimage_set.all()
			sentlist = []
			for ipil in itempicsidlist:
				sentlist.append(int(ipil))
			for p in oldPictureIdhandle:
				if int(p.id) not in sentlist:
					itemimage = ItemImage.objects.get(id=p.id)
					item.itemimage_set.remove(itemimage)
			#Update the picture item relationships
			for pics in sentlist:
				try:
					pichandle = ItemImage.objects.get(id=pics)
					pichandle.item = item
					pichandle.save()
				except:
					pihandle = ProductImage.objects.get(id=pics)
					pihandle.item.add(pihandle)
					pihandle.save()
			item.save()
			return HttpResponseRedirect("/listeditems")
		return HttpResponse("Error")
	return HttpResponse("Error")

def saveitem(request):
	item = Item.objects.get(id=request.POST['id'])
	if request.method == "POST" and request.user.is_authenticated():
		if (request.POST['action'] == "save"):
			if not SavedItem.objects.filter(user = BasicUser.objects.get(user=request.user),item=item).exists():
				si = SavedItem(user = BasicUser.objects.get(user=request.user),item=item)
				item.savedcount += 1
				si.save()
		else:
			if SavedItem.objects.filter(user = BasicUser.objects.get(user=request.user),item=item).exists():
				si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
				si.delete()
				item.savedcount -= 1
		return HttpResponse(json.dumps({'status':"100"}), mimetype='application/json')
	else:
		redirectURL = str('/login?next=/item/'+str(item.id)+"/details")
		return HttpResponse(json.dumps({'status':"400",'redirect':redirectURL}), mimetype='application/json')

@login_required
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
	itemqs = Item.objects.filter(devicecategory=category).order_by('price')
	if len(itemqs) > 5:
		more = True
	else:
		more = False
	#Get price range for price slider
	for itm in itemqs:
		pricelow = min(pricelow,itm.price)	
		pricehigh = max(pricehigh,itm.price)	
	return render_to_response('search.html',{'resultcount':len(itemqs),'more':more,'pricelow':pricelow,'pricehigh':pricehigh,'searchquery':searchquery,'items':itemqs[0:5],'categories':catlist,'category':category,'ind':industrysearch.name,'manufacturer':manufacturers},context_instance=RequestContext(request))

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
		results.append({'type':'product','name':itm.name,'category':itm.user.company,'mainimage':itm.mainimage.photo_small.url,'link':"/item/"+str(itm.id)+"/details"});
	
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
			results.append({'type':'product','name':itm.name,'category':itm.user.company,'mainimage':itm.mainimage.photo_small.url,'link':"/item/"+str(itm.id)+"/details"});
	return HttpResponse(json.dumps(results[0:10]), mimetype='application/json')

def customsearch(request):
	if request.method == "GET":
		searchword = request.GET['q']
		allitems = Item.objects.all()
		itemnames = []
		itemqs = []
		for p in allitems:
			itemnames.append(str(p.name))
			if difflib.SequenceMatcher(None,searchword,p.name.lower()).ratio() > .45:
				print difflib.SequenceMatcher(None,searchword,p.name.lower()).ratio()
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
		filters = {'page':request.GET['page'],'pricehigh':request.GET['pricehigh'],'pricelow':request.GET['pricelow'],'new':request.GET['new'],'refurbished':request.GET['refurbished'],'preowned':request.GET['preowned']}
		try:
			dc = DeviceCategory.objects.get(name=request.GET['category'])
			items = Item.objects.filter(devicecategory=dc).order_by('price')
		except:
			items = Item.objects.all()
		itemspassed = []
		for item in items:
			if item.price <= int(filters['pricehigh']) and item.price >= int(filters['pricelow']):
				if (item.type == 'new' and filters['new']=='true') or (item.type == 'refurbished' and filters['refurbished']=='true') or (item.type == 'preowned' and filters['preowned']=='true'):
					itemspassed.append(item)
		if len(itemspassed) > int(filters['page'])*5+5:
			more = True
		else:
			more = False
		resultscount = len(itemspassed)
		itemspassed = itemspassed[int(filters['page'])*5:int(filters['page'])*5+5]
	rts = render_to_string('productsearchitem.html', {'items':itemspassed})
	html = render(request, 'productsearchitem.html', {'items':itemspassed,'more':more},content_type="application/html")
	return HttpResponse(json.dumps({'result':rts,'more':more,'resultscount':resultscount}), mimetype='application/json')
	
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
	manufacturers = Manufacturer.objects.all()
	categories = DeviceCategory.objects.all()
	dict = {'manufacturers':manufacturers,'devicecategories':categories}
	if request.method == "GET":
		try:
			manufacturer = Manufacturer.objects.get(name=request.GET['manufacturer'])
			devicecategory = DeviceCategory.objects.get(name=request.GET['category'])
			for mans in manufacturers:
				if manufacturer.name == mans.name:
					mans.active = True
			for cats in categories:
				if devicecategory.name == cats.name:
					cats.active = True
			dict['model'] = request.GET['name']
		except:
			print 'Error with product get'
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
	related = Item.objects.filter(devicecategory = item.devicecategory).order_by('savedcount')[:6]
	dict = {'saved':saved,'item':item,'industry':industry,'related':related}
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		if item.user == bu:
			dict['userloggedin'] = bu
	return render_to_response('productdetails.html',dict,context_instance=RequestContext(request))

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
