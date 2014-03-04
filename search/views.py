from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from helper.haversine import *
from django.conf import settings
import math as math
import difflib, json, locale, time, urllib2
import medapp.settings as settings
import timeit
from helper.model_imports import *

###########################################
#### Search ###############################
###########################################	

#If 0, means it shows cats and subcats with 0 listings, 
showItems = 0
#Number of results per page
resultsPerPage = 8

def productsearch(request,industryterm,categoryterm,subcategoryterm):
	try:
		industry = Industry.objects.get(name=industryterm)
		category = None
		subcategory = None
		### Case 1: If you have no search criteria. redirect to the shop page
		if categoryterm == 'all' and subcategoryterm == 'all':
			return HttpResponseRedirect("/shop")
		### Case 2: If you only have a category, ie subcategory is all
		elif subcategoryterm == 'all':
			category = Category.objects.get(name=categoryterm)
			categoryname = category.displayname
			subcategoryname = subcategoryterm
			itemqs = Item.objects.filter(subcategory__in=category.subcategory_set.all()).filter(liststatus='active').order_by('creation_date').reverse()
			relatedItems = getSubcategories(category)
		### Case 3: If you have a subcategory
		else:
			subcategory = SubCategory.objects.get(name=subcategoryterm)
			# Set category if not set
			if categoryterm == 'all':
				category = subcategory.maincategory
			else:
				category = Category.objects.get(name=categoryterm)
			categoryname = category.displayname
			subcategoryname = subcategory.displayname
			itemqs = Item.objects.filter(subcategory=subcategory).filter(liststatus='active').order_by('price')
			relatedItems = getOtherSubcategories(subcategory)
		# Get price range, more boolean, and zipcodes
		pricerange = getPriceRange(itemqs)
		more = True if len(itemqs) > resultsPerPage else False
		zipcode = getDistances(request,itemqs[0:resultsPerPage])
		dict = {'zipcode':zipcode,'relatedItems':relatedItems,'resultcount':len(itemqs),'more':more,'pricerange':pricerange,'items':itemqs[0:resultsPerPage],'categoryname':categoryname,'subcategoryname':subcategoryname,'ind':industry,'category':category,'subcategory':subcategory}
		response = render_to_response('search/search.html',dict,context_instance=RequestContext(request))
		request.session['zipcode'] = zipcode
		return response
	except Exception,e:
		print e
		return HttpResponseRedirect('/shop')

def autosuggest(request):
	results=[]
	searchterm = request.GET['searchterm']
	#Spaces in the search return 0 results without the following line
	searchterm = searchterm.replace(' ','')
	industry = Industry.objects.get(id=1)
	
	# Find all categories that match the search term
	categories = Category.objects.filter(name__icontains=searchterm).filter(totalunits__gte=showItems)
	# Add all matched categories
	for cat in categories:
		results.append({'type':'category','name':cat.displayname,'results':'','link':"/productsearch/"+industry.name+"/"+cat.name+"/all"})
		results = results[0:5]
	 
	# Find all sub-categories that match the search term
	subcategories = SubCategory.objects.filter(name__icontains=searchterm).filter(totalunits__gte=showItems)
	for subcat in subcategories:
		results.append({'type':'subcategory','name':subcat.displayname,'results':'','link':"/productsearch/"+industry.name+"/all/"+subcat.name})
		results = results[0:10]
		
	# Find all items that match the search term
	# item = Item.objects.filter(subcategory__name__icontains=searchterm).filter(liststatus='active')
	# for itm in item:
	# 	dict = {'type':'product','name':itm.name,'category':itm.subcategory.displayname,'mainimage':checkMainImage(itm),'link':"/item/"+str(itm.id)+"/details"};
	# 	results.append(dict);
	
	# if len(results) == 0:
	# 	items = closeCategories(searchterm)
	# 	for itm in items:
	# 		dict = {'type':'product','name':itm.name,'category':itm.subcategory.displayname,'mainimage':checkMainImage(itm),'link':"/item/"+str(itm.id)+"/details"};
	# 		results.append(dict);

	# Do a relative match if no results are found
	if len(results) == 0:
		allcategories = Category.objects.filter(totalunits__gte=showItems)
		subcategories = SubCategory.objects.filter(totalunits__gte=showItems)
		for cat in categories:
			if difflib.SequenceMatcher(None,searchterm,cat.name.lower()).ratio() > .5:
				_cat = {'type':'category','name':cat.displayname,'results':'','link':"/productsearch/"+industry.name+"/"+cat.name+"/all"}
				results.append(_cat)
		for subcat in subcategories:
			if difflib.SequenceMatcher(None,searchterm,subcat.name.lower()).ratio() > .5:
				sub = {'type':'subcategory','name':subcat.displayname,'results':'','link':"/productsearch/"+industry.name+"/all/"+subcat.name}
				results.append(sub)
	return HttpResponse(json.dumps(results[0:15]), content_type='application/json')

def customsearch(request):
	if request.method == "GET":
		searchword = request.GET['q'].lower()
		if not searchword:
			return HttpResponseRedirect("/shop")
		if Category.objects.filter(name=searchword).exists():
			return HttpResponseRedirect('/productsearch/veterinary/'+str(searchword)+"/all")
		elif SubCategory.objects.filter(name=searchword).exists():
			return HttpResponseRedirect('/productsearch/veterinary/all/'+str(searchword))
		relatedItems = closeCategories(searchword)
		allitems = Item.objects.all().filter(liststatus='active').order_by('creation_date').reverse()
		items = filterItemsByQuery(searchword,allitems)
		zipcode = getDistances(request,items)
		industry = Industry.objects.get(id=1)
		searchquery = searchword.lower()
		catlist = getCategoriesAndQuantity()
		distance = getDistances(request,items)
		pricerange = getPriceRange(items)
		more = True if len(items) > resultsPerPage else False
		return render_to_response('search/search.html',{'custom':True,'zipcode':zipcode,'relatedItems':relatedItems,'resultcount':len(items),'searchquery':searchword,'more':more,'pricerange':pricerange,'searchquery':searchquery,'items':items[0:resultsPerPage],'categories':catlist,'ind':industry},context_instance=RequestContext(request))
	
def searchquery(request):
	if request.method == "GET":
		filters = {'sort':request.GET['sort'],
				'query':request.GET['query'],
				'page':request.GET['page'],
				'zipcode':request.GET['zipcode'],
				'distance':request.GET['distance'],
				'pricehigh':request.GET['pricehigh'],
				'pricelow':request.GET['pricelow'],
				'conditiontype':request.GET.getlist('conditiontype[]',[]),
				'contract':request.GET.getlist('contract[]',[])}
		if request.GET['custom'] == 'true':
			items = filterItemsByQuery(filters['query'],Item.objects.all().filter(liststatus='active').order_by('price'))
		else:
			subcategory = request.GET['subcategory']
			category = request.GET['category']
			items = getItems(category,subcategory)
		itemspassed = []
		for item in items:
			if checkPrice(item,int(filters['pricelow']),int(filters['pricehigh'])):
				if checkType(item,filters['conditiontype']) and checkWarranty(item,filters['contract']):
					if withinDistance(item,filters['zipcode'],filters['distance'],""):
						itemspassed.append(item)
		zipcode = getNewDistances(filters['zipcode'],itemspassed)
		itemspassed = sortItems(itemspassed,filters['sort'])
		more = True if len(itemspassed) > int(filters['page'])*resultsPerPage+resultsPerPage else False
		resultscount = len(itemspassed)
		itemspassed = itemspassed[int(filters['page'])*resultsPerPage:int(filters['page'])*resultsPerPage+resultsPerPage]
	rts = render_to_string('search/productsearchitem.html', {'items':itemspassed,'STATIC_URL':settings.STATIC_URL})
	return HttpResponse(json.dumps({'result':rts,'more':more,'resultscount':resultscount}), content_type='application/json')

def checkPrice(item,lowprice,highprice):
	passed = True if (item.price >= lowprice and item.price <= highprice) else False
	return passed

def checkType(item,conditiontypes):
	passed = True if item.conditiontype in conditiontypes else False;
	return passed

def checkWarranty(item,contracts):
	passed = True if item.contract in contracts else False;
	return passed

def sortItems(itemspassed,sortmethod):
	if sortmethod == 'mostrecent':
		itemspassed.sort(key=lambda x: x.creation_date, reverse=True)
	if sortmethod == 'leastrecent':
		itemspassed.sort(key=lambda x: x.creation_date, reverse=False)
	if sortmethod == 'distance':
		itemspassed.sort(key=lambda x: x.distance, reverse=False)
	if sortmethod == 'price-low':
		itemspassed.sort(key=lambda x: x.price, reverse=False)
	if sortmethod == 'price-high':
		itemspassed.sort(key=lambda x: x.price, reverse=True)
	if sortmethod == 'msrp-discount':
		itemspassed.sort(key=lambda x: x.msrp_discount(), reverse=False)
	return itemspassed
	
###########################################
#### Helper Functions for Search ##########
###########################################	

#Returns the list of device categories and the number of items in each one
def getCategoriesAndQuantity():
	catlist = Category.objects.filter(totalunits__gte=0).order_by('totalunits').reverse()
	return catlist

#Calculates the price range given a set of items
def getPriceRange(items):
	pricelow = 1000000
	pricehigh = 0
	if len(items) == 0:
		return [0,0]
	if len(items) == 1:
		return [int(items[0].price),int(items[0].price)]
	else:
		for itm in items:
			pricelow = min(pricelow,itm.price)	
			pricehigh = max(pricehigh,itm.price)
	return [int(math.floor(pricelow)),int(math.ceil(pricehigh))]

#Uses difflib to determine if an item matches a search query
#NEEDS TO BE REVISED FOR SCALABILITY
def filterItemsByQuery(searchword,items):
	if len(searchword) > 1:
		for p in items:
			if difflib.SequenceMatcher(None,searchword,p.name.lower()).ratio() < .35:
				items = items.exclude(pk=p.pk)
	return items

#Set the main image to none if there is no main image
def checkMainImage(item):
	if item.mainimage:
		return item.mainimage.photo_small.url
	else:
		return None	
	
###########################################
#### Functions for related items ##########
###########################################	

def getItems(categoryterm,subcategoryterm):
	if subcategoryterm == 'all':
		category = Category.objects.get(name=categoryterm)
		itemqs = Item.objects.filter(subcategory__in=category.subcategory_set.all()).filter(liststatus='active').order_by('price')
	elif categoryterm == 'all':
		subcategory = SubCategory.objects.get(name=subcategoryterm)
		itemqs = Item.objects.filter(subcategory=subcategory).filter(liststatus='active').order_by('price')
	else:
		category = Category.objects.get(name=categoryterm)
		subcategory = SubCategory.objects.get(name=subcategoryterm)
		itemqs = Item.objects.filter(subcategory=subcategory).filter(liststatus='active').order_by('price')
	return itemqs

def closeCategories(searchterm):
	close = []
	for sub in SubCategory.objects.filter(totalunits__gte = 1):
		ratio = difflib.SequenceMatcher(None,searchterm,sub.displayname.lower()).ratio()
		if ratio > .3:
			close.append({'obj':sub,'type':'subcategory','match': ratio})
	for cat in Category.objects.filter(totalunits__gte = 1):
		ratio = difflib.SequenceMatcher(None,searchterm,cat.displayname.lower()).ratio()
		if ratio > .3:
			close.append({'obj':cat,'type':'category','match': ratio})
	close = sorted(close, key=lambda k: k['match'],reverse=True)
	return close[0:6]

#Takes in a category 
def getSubcategories(cathandle):
	related = []
	for sub in cathandle.subcategory_set.filter(totalunits__gte = 1):
		related.append({'obj':sub,'type':'subcategory'})
	return related

#Takes in a subcategory
def getOtherSubcategories(subcathandle):
	related = []
	for sub in subcathandle.maincategory.subcategory_set.filter(totalunits__gte = 1):
		related.append({'obj':sub,'type':'subcategory'})
	return related

###########################################
#### Zipcode + Distance Functions #########
###########################################	

# Get distances given a use request
def getDistances(request,items):
	zipcode = None
	#First check is user is logged in
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		userzipcode = "%05d" % bu.zipcode
		if len(userzipcode) == 5:
			zipcode = userzipcode
	# Then check the session variables
	elif 'zipcode' in request.session:
		zipcode = request.session['zipcode']
	#Finally call the API
	else:
		newzipcode = callZipcodeAPI(request)
		if newzipcode:
			if len(newzipcode) == 5:
				zipcode = userzipcode
	#If one of three gave us a zipcode, find distances
	if zipcode != 'None' and zipcode:	
		zips = []
		for itm in items:
			zips.append(itm.user.zipcode)
		latlongs = LatLong.objects.filter(zipcode__in=zips)
		for item in items:
			item.distance = haversineDistance(zipcode,item.user.zipcode,latlongs)
	return zipcode

# Get distances given items and a custom zipcode
def getNewDistances(zipcode,items):
	zips = []
	for itm in items:
		zips.append(itm.user.zipcode)
	latlongs = LatLong.objects.filter(zipcode__in=zips)
	for item in items:
		item.distance = haversineDistance(zipcode,item.user.zipcode,latlongs)
	return zipcode

# Given an item, zipcode, and distance, determine if the item and zip are within the distance
def withinDistance(item,zipcode,distance,latlongs):
	if int(distance) < 0:
		return True
	else:
		dist = haversineDistance(zipcode,item.user.zipcode,latlongs)
		if dist < int(distance):
			return True
		else:
			return False
	
# Get the user's zipcode if they are not logged in or have it saved as a cookie
def callZipcodeAPI(request):
	try:
	  remote_addr = request.META['REMOTE_ADDR']
	  url = "http://www.iptolatlng.com?ip="+remote_addr+"&type=json"
	  result = urllib2.urlopen(url)
	  response = result.read()
	  list = json.loads(response)
	  if list['zip'] != "None":
	  	return list['zip']
	  else:
	  	return None
	except urllib2.URLError, e:
	  return None


	
	