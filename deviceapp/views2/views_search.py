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
from haversine import *
from django.conf import settings
import json
import math
import difflib
import locale
import time
import medapp.settings as settings

###########################################
#### Search ###############################
###########################################	


def productsearch(request,industryterm,categoryterm,subcategoryterm):
	catlist = getCategoriesAndQuantity()
	industry = Industry.objects.get(name=industryterm)
	# Case 1: If you have no search criteria
	if categoryterm == 'all' and subcategoryterm == 'all':
		itemqs = Item.objects.filter(liststatus='active').order_by('price')
		categoryname = categoryterm
		subcategory = subcategoryterm
	# Case 2: If you only have a category, ie subcategory is all
	elif subcategoryterm == 'all':
		category = Category.objects.get(name=categoryterm)
		categoryname = category.displayname
		itemqs = Item.objects.filter(subcategory__in=category.subcategory_set.all()).filter(liststatus='active').order_by('price')
	#Case 3: If you have a subcategory and a category
	else:
		subcategory = SubCategory.objects.get(name=subcategoryterm)
		category = Category.objects.get(name=categoryterm)
		categoryname = category.displayname
		subcategoryname = subcategory.displayname
		itemqs = Item.objects.filter(subcategory=subcategory).order_by('price')
	#Get price range, more boolean, and zipcodes
	pricerange = getPriceRange(itemqs)
	more = True if len(itemqs ) > 5 else False
	zipcode = getDistances(request,itemqs[0:10])
	dict = {'zipcode':zipcode,'resultcount':len(itemqs),'more':more,'pricerange':pricerange,'items':itemqs[0:10],'categories':catlist,'categoryname':categoryname,'subcategoryname':subcategoryname,'ind':industry}
	return render_to_response('search/search.html',dict,context_instance=RequestContext(request))

def autosuggest(request):
	results=[]
	searchterm = request.GET['searchterm']
	industry = Industry.objects.get(id=1)
	
	#Find all categories that match the search term
	categories = Category.objects.filter(name__icontains=searchterm).filter(totalunits__gte=0)
	#Add all matched categories
	for cat in categories:
		results.append({'type':'category','name':cat.displayname,'link':"/productsearch/"+industry.name+"/"+cat.name+"/all"})
		results = results[0:5]
	
	#Find all sub-categories that match the search term
	subcategories = SubCategory.objects.filter(name__icontains=searchterm).filter(totalunits__gte=0)
	for subcat in subcategories:
		results.append({'type':'subcategory','name':subcat.displayname,'category':subcat.category.displayname,'link':"/productsearch/"+industry.name+"/"+subcat.category.name+"/"+subcat.name})
		results = results[0:10]
		
	#Find all items that match the search term
	item = Item.objects.filter(subcategory__name__icontains=searchterm)
	for itm in item:
		dict = {'type':'product','name':itm.name,'category':itm.user.company,'mainimage':checkMainImage(itm),'link':"/item/"+str(itm.id)+"/details"};
		results.append(dict);
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
			results.append({'type':'product','name':itm.name,'category':itm.user.company,'mainimage':checkMainImage(itm),'link':"/item/"+str(itm.id)+"/details"});
	return HttpResponse(json.dumps(results[0:15]), mimetype='application/json')

def customsearch(request):
	if request.method == "GET":
		searchword = request.GET['q']
		allitems = Item.objects.all().order_by('price')
		items = filterItemsByQuery(searchword,allitems)
		zipcode = getDistances(request,items)
		industry = Industry.objects.get(id=1)
		searchquery = searchword
		catlist = getCategoriesAndQuantity()
		manufacturers = Manufacturer.objects.all()
		distance = getDistances(request,items)
		pricerange = getPriceRange(items)
		more = True if len(items) > 5 else False
		return render_to_response('search/search.html',{'custom':'on','zipcode':zipcode,'resultcount':len(items),'searchquery':searchword,'more':more,'pricerange':pricerange,'searchquery':searchquery,'items':items[0:5],'categories':catlist,'ind':industry,'manufacturer':manufacturers},context_instance=RequestContext(request))
	
def searchquery(request):
	itemdict = []
	if request.method == "GET":
		itemdict = []
		filters = {'sort':request.GET['sort'],'query':request.GET['query'],'page':request.GET['page'],'zipcode':request.GET['zipcode'],'distance':request.GET['distance'],'pricehigh':request.GET['pricehigh'],'pricelow':request.GET['pricelow'],'new':request.GET['new'],'refurbished':request.GET['refurbished'],'preowned':request.GET['preowned']}
		print 'searchquery'
		print request.GET['subcategory']
		try:
			if request.GET['subcategory'] != 'all':
				sc = SubCategory.objects.get(name=request.GET['subcategory'])
				items = Item.objects.filter(subcategory=sc).order_by('price')
			else:
				category = Category.objects.get(name=request.GET['category'])
				print category
				print category.subcategory_set.all()
				items = Item.objects.filter(subcategory__in=category.subcategory_set.all()).order_by('price')
		except:
			items = filterItemsByQuery(filters['query'],Item.objects.all().order_by('price'))
		itemspassed = []
		for item in items:
			if item.price <= int(filters['pricehigh']) and item.price >= int(filters['pricelow']):
				if (item.type == 'new' and filters['new']=='true') or (item.type == 'refurbished' and filters['refurbished']=='true') or (item.type == 'preowned' and filters['preowned']=='true'):
					if withinDistance(item,filters['zipcode'],filters['distance'],""):	
						itemspassed.append(item)
		zipcode = getNewDistances(filters['zipcode'],itemspassed)
		if filters['sort'] == 'mostrecent':
			itemspassed.sort(key=lambda x: x.listeddate, reverse=True)
		if filters['sort'] == 'leastrecent':
			itemspassed.sort(key=lambda x: x.listeddate, reverse=False)
		if filters['sort'] == 'distance':
			itemspassed.sort(key=lambda x: x.distance, reverse=False)
		more = True if len(itemspassed) > int(filters['page'])*5+5 else False
		resultscount = len(itemspassed)
		itemspassed = itemspassed[int(filters['page'])*5:int(filters['page'])*5+5]
	rts = render_to_string('search/productsearchitem.html', {'items':itemspassed,'STATIC_URL':settings.STATIC_URL})
	return HttpResponse(json.dumps({'result':rts,'more':more,'resultscount':resultscount}), mimetype='application/json')


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
	return [int(pricelow),int(pricehigh)]

#Uses difflib to determine if an item matches a search query
#NEEDS TO BE REVISED FOR SCALABILITY
def filterItemsByQuery(searchword,items):
	for p in items:
		if difflib.SequenceMatcher(None,searchword,p.name.lower()).ratio() < .35:
			items = items.exclude(pk=p.pk)
	return items

#Get distances given a use request
def getDistances(request,items):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		zipcode = "%05d" % bu.zipcode
		zips = []
		for itm in items:
			zips.append(bu.zipcode)
		latlongs = LatLong.objects.filter(zipcode__in=zips)
		for item in items:
			item.distance = haversineDistance(zipcode,item.user.zipcode,latlongs)
	else:
		zipcode = 00000
	return zipcode

#Get distances given items and a custom zipcode
def getNewDistances(zipcode,items):
	zips = []
	for itm in items:
		zips.append(itm.user.zipcode)
	latlongs = LatLong.objects.filter(zipcode__in=zips)
	for item in items:
		item.distance = haversineDistance(zipcode,item.user.zipcode,latlongs)
	return zipcode

#Given an item, zipcode, and distance, determine if the item and zip are within the distance
def withinDistance(item,zipcode,distance,latlongs):
	if int(distance) < 0:
		return True
	else:
		dist = haversineDistance(zipcode,item.user.zipcode,latlongs)
		if dist < int(distance):
			return True
		else:
			return False

#Set the main image to none if there is no main image
def checkMainImage(item):
	if item.mainimage:
		return item.mainimage.photo_small
	else:
		return None	
	
	
	
	
	
	
	