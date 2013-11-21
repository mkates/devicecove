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
	