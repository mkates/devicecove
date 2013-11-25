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


####################################################################################################
#Save an image to S3 and send back the id of the userimage object, so when the item post is completed
#it can use the id to attach an item to the userimage object
####################################################################################################
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

def existingproductcheck(request):
	if request.method == "GET":
		manufacturer = request.GET['manufacturer']
		category = request.GET['category']
		manufacturer = Manufacturer.objects.get(name = manufacturer)
		category = DeviceCategory.objects.get(name=category)
		products = Product.objects.filter(devicecategory=category).filter(manufacturer=manufacturer)
		product_names = []
		for pnames in products:
			product_names.append(pnames.name)
		return HttpResponse(json.dumps({'products':product_names}), mimetype='application/json')

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