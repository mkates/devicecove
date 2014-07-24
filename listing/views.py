from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from django.utils.timezone import utc
import json, re, string, math, difflib, locale, time
from fuzzywuzzy import fuzz, process
from listing.models import *
import checkout.views as checkoutview
import emails.views as email_view
import helper.commission as commission
from helper.model_imports import *
from django.db.models import Q

###########################################
#### Listing Pages  #######################
###########################################

##### Predefined Search Pages #############

# Search by a category
def category(request,category):
	category = Category.objects.get(name=category)
	child_categories = allCategoriesInTree(category) # Gets all categories below it in the tree
	products = Product.objects.filter(category__in=child_categories) # Get all the products in the child_categories
	dictionary = {'child_categories':child_categories,'category':category}
	details = getDetailsFromSearch(products) # Get details for each product
	return render_to_response('search/search2.html',dict(dictionary.items()+details.items()),context_instance=RequestContext(request))

# Bring up the company pages if they select a company #
def manufacturer(request,manufacturer):
	manufacturer = Manufacturer.objects.get(name=manufacturer)
	products = Product.objects.all()[0:7] # Temporary list of products, will replace with the company's products
	return render_to_response('search/company.html',{'manufacturer':manufacturer,'products':products},context_instance=RequestContext(request))

def ingredient(request,ingredient):
	pass

def product(request,product):
	pass

def item(request,item):
	pass



##### Search Algorithms #############

# Autosuggest search #
# TODO: augment with cache for commonly searched for items
def autosuggest(request):
	searchterm = request.GET.get('searchterm','')
	bestmatches = relatedProductsFromSearchWord(searchterm,10)
	dict = []
	# Generate the links from the matches
	for items in bestmatches:
		# Item format ('equipose','90','product')
		if items[2] == 'category':
			category = Category.objects.get(name=items[0])
			dict.append({'type':'category','name':category.displayname,'link':category.name})
		elif items[2] == 'manufacturer':
			manufacturer = Manufacturer.objects.get(name=items[0])
			dict.append({'type':'manufacturer','name':manufacturer.displayname,'link':manufacturer.name})
		elif items[2] == 'item':
			item = Item.objects.get(manufacturer_no=items[0])
			dict.append({'type':'item','name':item.displayname + item.manufacturer_no,'link':item.name})
		elif items[2] == 'product':
			product = Product.objects.get(name=items[0])
			mainimage = settings.STATIC_URL+"img/placeholder_pics/"+str(product.id)+".gif" # Temporarily image display
			dict.append({'type':'product','name':product.displayname,'link':product.name,'mainimage':mainimage,'category':product.category.displayname})
	return HttpResponse(json.dumps(dict), content_type='application/json')


# Returns the eligible items based on the category and the filters
def filterSearch(category,filters):
	category = Category.objects.get(name=category)
	child_categories = allCategoriesInTree(category)
	products = Product.objects.filter(category__in=child_categories)
	eligibleItems = []
	for product in products:
		items = product.item_set.all()
		if product.averagerating < int(filters['stars']-1)*10: # Product Rating
			continue
		if filters['manufacturers']: # Manufacturer
			if product.manufacturer not in filters['manufacturers']:
				continue
		eligibleItems.append(product)
	return eligibleItems

# Find related products with a custom search, GOAL_AMOUNT is the number of results to return
def relatedProductsFromSearchWord(searchword,GOAL_AMOUNT):
	results = []

	# Categories
	categories = Category.objects.values_list('name',flat=True)
	results = results + getTopMatches(results,searchword,categories,'category',10)
	# Product
	products = Product.objects.values_list('name',flat=True)
	results= results+ getTopMatches(results,searchword,products,'product',20)
	# Item
	items = Item.objects.values_list('manufacturer_no',flat=True)
	results= results+ getTopMatches(results,searchword,items,'item',3)
	# Manufacturer
	manufacturers = Manufacturer.objects.values_list('name',flat=True)
	results= results+ getTopMatches(results,searchword,manufacturers,'manufacturer',10)
	# Ingredients
	ingredients = Ingredient.objects.values_list('name',flat=True)

	# Sort and limit results
	results= results+ getTopMatches(results,searchword,items,'ingredients',5)
	sorted_results = sorted(results, key=lambda tup: tup[1], reverse=True)[0:GOAL_AMOUNT]
	return sorted_results

### Given a list of strings and a word, find the n best matches ###
def getTopMatches(results,searchword,flat_objs,name,limit):
	top_ten = process.extract(searchword,flat_objs,limit=limit)
	list = [((tt[0],tt[1],name) if int(tt[1])>60 else None) for tt in top_ten] 
	return filter(None,list)

### Get Details from a search ####
def getDetailsFromSearch(products):
	manufacturers = []
	lowprice, highprice = None, None
	for product in products:
		if product.manufacturer not in manufacturers:
			manufacturers.append(product.manufacturer)
		details = getItemDetailsFromAProduct(product)
		if not lowprice or details['lowprice'] < lowprice:
			lowprice = details['lowprice']
		if not highprice or details['highprice'] > highprice:
			highprice = details['highprice']
		product.details = details
	return {'manufacturers':manufacturers,'lowprice':lowprice,'highprice':highprice,'products':products}

### Given a product, get details from all the item's listings ####
def getItemDetailsFromAProduct(product):
	items = product.item_set.all()
	lowprice,highprice = None, None
	msrp_lowprice,msrp_highprice = None,None
	suppliers = []
	quantity = 0
	for item in items:
		if not msrp_lowprice or item.msrp_price < msrp_lowprice:
			msrp_lowprice = item.msrp_price
		if not msrp_highprice or item.msrp_price > msrp_highprice:
			msrp_highprice = item.msrp_price 
		inventories = item.inventory_set.all()
		for inventory in inventories:
			if inventory.supplier not in suppliers:
				suppliers.append(inventory.supplier)
			quantity += inventory.quantity_available
			if not lowprice or inventory.base_price < lowprice:
				lowprice = inventory.base_price
			if not highprice or inventory.base_price > highprice:
				highprice = inventory.base_price
	return {'lowprice':lowprice,'highprice':highprice,'msrp_lowprice':msrp_lowprice,'msrp_highprice':msrp_highprice,'quantity':quantity,'suppliers':suppliers}


##### Search Helper Methods #############


# Finds all descendants of a category
def allCategoriesInTree(category):
	# TODO!!! Eventually here, pre store all children in the database in a field
	categories = [category]
	for cat in category.category_set.all():
		categories.append(cat)
	return categories

























@login_required
def newlisting(request,listingtype):
	if request.user.is_authenticated:
		bu = request.user.basicuser
		if listingtype == 'newequipment':
			item = NewEquipment(user=bu)
		if listingtype == 'usedequipment':
			item = UsedEquipment(user=bu)
		if listingtype == 'pharmaitem':
			item = PharmaItem(user=bu)
		item.save()
		if not (bu.businesstype and bu.phonenumber and bu.company):
 			return HttpResponseRedirect('/list/business/'+str(item.id))
		return HttpResponseRedirect('/list/describe/'+str(item.id))


#Business Description
@login_required
def listbusiness(request,itemid):
	item = Item.objects.get(id=itemid)
	return render_to_response('item/item_business.html',{'item':item},context_instance=RequestContext(request))

#Save Business Description
@login_required
def savebusiness(request,itemid):
	item = Item.objects.get(id=itemid)
	if itemOwner(request,itemid) and request.method=="POST":
		bu = request.user.basicuser
		bu.company = request.POST.get('company','')
		bu.phonenumber = int(re.sub("[^0-9]", "",request.POST.get("phonenumber","")))
		bu.businesstype = request.POST.get('business','')
		bu.website = request.POST.get('website','')
		companyimage = request.FILES.get("companyimage",'')
		bu.mainimage = companyimage if companyimage else None
		bu.save()
		return HttpResponseRedirect('/list/describe/'+str(itemid))
	return HttpResponseRedirect('/listintro')

#Item Description
@login_required
def listitemdescribe(request,itemid):
	if itemOwner(request,itemid):
		item = Item.objects.get(id=itemid)
		item.liststage = max(1,item.liststage)
		item.save()
		dict = {'item':item,'categories':Category.objects.all(),'manufacturers':Manufacturer.objects.all(),'range':reversed(range(1980,2015))}
		categories = Category.objects.all()
		return render_to_response('item/item_describe.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/listintro')

@login_required
def savedescribe(request,itemid):
	try:
		if request.method == "POST" and itemOwner(request,itemid):
			submitcode = 600 if int(request.POST['submitcode']) == 600 else 700
			item = Item.objects.get(id=itemid)
			item_handle = item.item_handle()
			item_type = item.item_type()
			subcategory = request.POST.get('subcategory','0')
			if subcategory != '0':
				item_handle.subcategory = SubCategory.objects.get(name=subcategory)
			item_handle.manufacturer = request.POST.get('manufacturer','')
			item_handle.name = request.POST.get('name','')
			item_handle.modelyear = request.POST.get('modelyear',2014)
			if item_type == 'usedequipment':
				item_handle.conditiontype = request.POST.get('conditiontype','preowned')
				item_handle.serialno = request.POST.get('serialnumber',None)
				item.originalowner = True if request.POST.get('originalowner','True')=='True' else False
			elif item_type == 'newequipment':
				item_handle.quantity = request.POST.get('quantity',1)
			item_handle.save()
			return HttpResponse(submitcode)
		return HttpResponse(500)
	except Exception, e:
		print e
		return HttpResponse(500)

#Item Details
@login_required
def listitemdetails(request,itemid):
	if itemOwner(request,itemid):
		item = Item.objects.get(id=itemid)
		item.liststage = max(2,item.liststage)
		item.save()
		dict = {'item':item}
		return render_to_response('item/item_details.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/listintro')


@login_required
def savedetails(request,itemid):
	try:
		if request.method == "POST" and itemOwner(request,itemid):
			submitcode = 600 if int(request.POST['submitcode']) == 600 else 700
			item = Item.objects.get(id=itemid)
			item_handle = item.item_handle()
			item_type = item.item_type()
			item_handle.whatsincluded = request.POST.get('whatsincluded','')
			item_handle.productdescription = request.POST.get('productdescription','')
			item_handle.contract = request.POST.get('contract','')
			item_handle.contractdescription = request.POST.get('contractdescription','')
			if item_type == 'usedequipment':
				item_handle.conditionquality = request.POST.get('conditionquality',3)
				item_handle.conditiondescription = request.POST.get('conditiondescription','')
			item_handle.save()
			return HttpResponse(submitcode)
		return HttpResponse(500)
	except:
		return HttpResponse(500)
	
#Item Photos
@login_required
def listitemphotos(request,itemid):
	if itemOwner(request,itemid):
		item = Item.objects.get(id=itemid)
		item.liststage = max(3,item.liststage)
		item.save()
		dict = {'item':item}
		return render_to_response('item/item_photos.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/listintro')
	
# Delete an image by dereferencing it from an item
# The image still remains in the databse
@login_required
def deleteimage(request):
	if request.method == "POST":
		itemimg = Image.objects.get(id=request.POST['imageid'])
		item = Item.objects.get(id=request.POST['itemid'])
		bu = request.user.basicuser
		# Check if image belongs to the user
		if item.user == bu:
			if item.mainimage == itemimg:
				item.mainimage = None
				item.save()
			itemimg.item.remove(item)
			if item.mainimage == None:
				if item.image_set.exists():
					item.mainimage = item.image_set.all()[0]
					item.save()
		dict = {'status':201,'data':generateImageList(item)}
		return HttpResponse(json.dumps(dict), content_type='application/json')
	return HttpResponseRedirect('/list/photos/'+str(item.id))

#The request contains the image id of the new main image
@login_required
def setmainimage(request):
	if request.method == "POST":
		itemimg = Image.objects.get(id=request.POST['imageid'])
		item = Item.objects.get(id=request.POST['itemid'])
		bu = request.user.basicuser
		#Check if image belongs to the user
		if item.user == bu:
			item.mainimage = itemimg
			item.save()
		dict = {'status':201,'data':generateImageList(item)}
		return HttpResponse(json.dumps(dict), content_type='application/json')
	return HttpResponseRedirect('/list/photos/'+str(item.id))
	
# Save an uploaded image and send back the image icon for display
@login_required
def imageupload(request,itemid):
	try:
		if itemOwner(request,itemid):
			item = Item.objects.get(id=itemid)
			for file in request.FILES.getlist('files'):
				extension = file.name.split('.')[1]
				extension = extension.lower()
				if not (extension == 'png' or extension == 'jpg'):
					return HttpResponse(json.dumps({'status':500,'error':'filetype'}), content_type='application/json')
				if file.size > 4194304:
					return HttpResponse(json.dumps({'status':500,'error':'filesize'}), content_type='application/json')
				if item.image_set.count() > 10:
					return HttpResponse(json.dumps({'status':500,'error':'filecount'}), content_type='application/json')
				ui = Image(photo=file,photo_small=file,photo_medium=file)
				ui.save()
				ui.item.add(item)
				ui.save()
				# Make it the main image if there is no main image
				if item.mainimage == None:
					item.mainimage = ui
					item.save()
			dict = {'status':201,'data':generateImageList(item)}
			return HttpResponse(json.dumps(dict), content_type='application/json')
	except Exception,e:
		print e
		return HttpResponse(json.dumps({'status':500,'error':'error'}), content_type='application/json')


### Generates a list of the item's images and their relevant information ###
def generateImageList(item):
	image_list = []
	images = item.image_set.all()
	for image in images:
		main = True if item.mainimage == image else False
		image_list.append({'id':image.id,'url':image.photo_medium.url,'main':main})
	return image_list

#Item Logistics
@login_required
def listitemlogistics(request,itemid):
	if itemOwner(request,itemid):
		item = Item.objects.get(id=itemid)
		item.liststage = max(4,item.liststage)
		item.save()
		charities = Charity.objects.all()
		dict = {'item':item,'logistics':True,'charities':charities}
		categories = Category.objects.all()
		return render_to_response('item/item_logistics.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/listintro')

@login_required
def savelogistics(request,itemid):
	try:
		if request.method == "POST" and itemOwner(request,itemid):
			submitcode = 600 if int(request.POST['submitcode']) == 600 else 700
			item = Item.objects.get(id=itemid)
			item_handle = item.item_handle()
			item_type = item.item_type()
			item_handle.shippingincluded = True if request.POST.get('shippingincluded','True') == 'True' else False
			price = request.POST.get('inputlistprice','0')
			if price:
				new_price = int(round(float(price.replace(",","").replace("$","0")),2)*100)
				if item.price and item.price != new_price and item.liststatus == "active":
					pc = PriceChange(item=item,original_price=item.price,new_price=new_price)
					pc.save()
				item_handle.price = new_price
			if item_type == 'usedequipment':
				item_handle.offlineviewing = True if request.POST.get('offlineviewing',False) else False
				item_handle.max_price = max(item_handle.max_price,item.price)
			msrp_price = request.POST.get('inputmsrpprice','0')
			if msrp_price:
				item_handle.msrp_price = int(round(float(msrp_price.replace(",","").replace("$","0")),2)*100)
			item_handle.charity = True if request.POST.get('charity',False) else False
			item_handle.charity_name = Charity.objects.get(name=request.POST.get('charity_name','Any'))
			if request.POST.get('promocode',''):
				if PromoCode.objects.filter(code=request.POST.get('promocode'),active=True).exists():
					item_handle.promo_code = PromoCode.objects.get(code=request.POST.get('promocode'))
			item_handle.save()
			return HttpResponse(submitcode)
		return HttpResponse(500)
	except Exception,e:
		print e
		return HttpResponse(500)


@login_required
def addPromoCode(request,itemid):
	dict = {}
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and item.user == request.user.basicuser: 
		promocode = request.POST.get('promocode','')
		promocode = promocode.lower()
		try:
			pc = PromoCode.objects.get(code=promocode.lower())
			if pc.active:
				item.promo_code = pc
				item.save()
				dict = {'status':201,'code':pc.code,'message':pc.promo_text}
			else:
				dict = {'status':400,'message':"You're too late! This code has expired. Sorry!"}
		except:
			dict = {'status':500,'message':'The code you entered is invalid'}
	else:
		dict = {'status':500,'message':'You are not the owner of the item'}
	return HttpResponse(json.dumps(dict), content_type='application/json')
			
#Item Preview
@login_required
def listitempreview(request,itemid):
	if itemOwner(request,itemid):
		item = Item.objects.get(id=itemid)
		item.liststage = max(5,item.liststage)
		item.save()
		dict = {'item':item,'preview':True}
		categories = Category.objects.all()
		return render_to_response('item/item_preview.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/listintro')

@login_required
def activateListing(request,itemid):
	if request.method == "POST" and itemOwner(request,itemid):
		item = Item.objects.get(id=itemid)
		if not item.tos:
			return render_to_response('item/item_tos.html',{'item':item},context_instance=RequestContext(request))
		item.liststatus = 'active'
		item.save()
		return HttpResponseRedirect('/item/'+itemid+'/details')
	return HttpResponseRedirect('/listintro')

@login_required
def deleteListing(request,itemid):
	if request.method == "POST" and itemOwner(request,itemid):
		item = Item.objects.get(id=itemid)
		item.delete()
		return HttpResponseRedirect('/account/listings/incomplete')
	return HttpResponseRedirect('/listintro')

@login_required
def tosListing(request,itemid):
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and itemOwner(request,itemid):
		if request.POST.get('tos',''):
			item.liststatus = 'active'
			item.creation_date = datetime.now()
			item.tos = True
			item.save()
			email_view.composeEmailListingConfirmation(request.user.basicuser,item)
			return HttpResponseRedirect('/item/'+itemid+'/details')
	return HttpResponseRedirect('/listintro')
			
###########################################
#### Product Pages ########################
###########################################

def itemdetails(request,itemid):
	item = Item.objects.get(id=int(itemid))
	#If item shouldn't be viewable, different if its the lister looking
	if request.user.is_authenticated():
		if request.user.basicuser == item.user:
			if item.liststatus not in ['active','unsold','sold']:
				return HttpResponseRedirect("/error/itemdoesnotexist")
	else:
		if item.liststatus != "active" and item.liststatus != "sold":
			return HttpResponseRedirect("/error/itemdoesnotexist")
	industry = Industry.objects.get(id=1)
	saved = False
	authorized = False
	shoppingcart = checkoutview.getShoppingCart(request)
	if request.user.is_authenticated():
		bu = request.user.basicuser
		if SavedItem.objects.filter(user=bu,item=item).exists():
			saved = True
		if item.user != bu:
			item.views += 1
			item.save()
		if BuyAuthorization.objects.filter(seller=item.user,item=item,buyer=bu).exists():
			authorized = True
	related = Item.objects.filter(subcategory = item.subcategory).filter(liststatus='active').filter(~Q(id=itemid)).order_by('views')[:9]
	dict = {'saved':saved,'item':item,'industry':industry,'related':related,'authorized':authorized}
	#Is the item in their shopping cart?
	isInShoppingCart = False
	if shoppingcart:
		for cartitem in shoppingcart.cartitem_set.all():
			if cartitem.item == item:
				isInShoppingCart = True
	dict['isinshoppingcart'] = isInShoppingCart
	return render_to_response('product/productdetails.html',dict,context_instance=RequestContext(request))

###########################################
#### Listing Actions  #####################
###########################################


@login_required
def markAsSold(request,itemid):
	item = Item.objects.get(id=itemid)
	if request.method == "POST" and item.user == request.user.basicuser:
		if item.liststatus == 'active':
			item.liststatus = 'sold'
			item.save()
	return HttpResponseRedirect(request.POST['page'])


###########################################
#### User Function Pages ##################
###########################################

#### Checks if a request's user is the creator of the item
def itemOwner(request,itemid):
	try:
		bu = request.user.basicuser
		item = Item.objects.get(id=itemid)
		# Only certain items can be edited
		if item.liststatus in ['disabled','sold','deleted']:
			return False
		if item.user == bu:
			return True
		else:
			return False
	except:
		return False