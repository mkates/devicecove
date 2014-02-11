from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
import views_checkout as checkoutview
import views_email as email_view
import commission as commission
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import json, re, string, math, difflib, locale, time

###########################################
#### Listing Pages  #######################
###########################################

#Intro Page
def listintro(request):
	category = Category.objects.all().extra(order_by = ['displayname'])
	return render_to_response('product/listintro.html',{'categories':category},context_instance=RequestContext(request))

def getsubcategories(request):
	category = Category.objects.get(name=request.GET['category'])
	subcategories = SubCategory.objects.filter(category=category)
	dict = {}
	for sub in subcategories:
		dict[sub.name] = sub.displayname
	return HttpResponse(json.dumps(dict), content_type='application/json')

@login_required
def listproduct(request,subcategory):
	if request.user.is_authenticated:
		bu = BasicUser.objects.get(user=request.user)
		subcategory = SubCategory.objects.get(name=subcategory)
 		newitem = Item(user=bu,
 						subcategory=subcategory,
 						originalowner=True,
 						offlineviewing=False,
 						contract="none",
 						msrp_price = 0,
 						price = 0,
 						conditiontype = "preowned",
 						conditionquality = 3,
 						shippingincluded = True,
 						liststatus = 'incomplete',
 						liststage = 0,
 						savedcount = 0)
 		newitem.save()
 		if not (bu.businesstype and bu.phonenumber and bu.company):
 			return HttpResponseRedirect('/list/business/'+str(newitem.id))
		return HttpResponseRedirect('/list/describe/'+str(newitem.id))
	return HttpResponse(request.method)

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
			subcategory = request.POST.get('subcategory','0')
			if subcategory != '0':
				item.subcategory = SubCategory.objects.get(name=request.POST.get('subcategory',''))
			item.manufacturer = request.POST.get('manufacturer','')
			item.name = request.POST.get('name','')
			item.serialno = request.POST.get('serialnumber','None')
			item.modelyear = request.POST.get('modelyear',2014)
			item.conditiontype = request.POST.get('conditiontype','preowned')
			item.quantity = request.POST.get('quantity',1)
			# New items can't be viewed offline
			if item.conditiontype == 'new':
				item.offlineviewing = False
				item.conditionquality = 5
			else:
				item.quantity = 1
				if item.conditionquality == 5:
					item.conditionquality = 3
			item.originalowner = True if request.POST.get('originalowner','True')=='True' else False
			item.save()
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
		categories = Category.objects.all()
		return render_to_response('item/item_details.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/listintro')


@login_required
def savedetails(request,itemid):
	try:
		if request.method == "POST" and itemOwner(request,itemid):
			submitcode = 600 if int(request.POST['submitcode']) == 600 else 700
			item = Item.objects.get(id=itemid)
			item.whatsincluded = request.POST.get('whatsincluded','')
			item.conditionquality = request.POST.get('conditionquality',3)
			item.conditiondescription = request.POST.get('conditiondescription','')
			item.productdescription = request.POST.get('productdescription','')
			item.contract = request.POST.get('contract','')
			item.contractdescription = request.POST.get('contractdescription','')
			item.save()
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
		categories = Category.objects.all()
		return render_to_response('item/item_photos.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect('/listintro')
	
#Delete an image by dereferencing it from an item
#The image still remains in the databse
@login_required
def deleteimage(request):
	if request.method == "POST":
		imageid = request.POST['imageid']
		itemimg = Image.objects.get(id=imageid)
		bu = BasicUser.objects.get(user = request.user)
		if itemimg.item.user == bu:
			if itemimg.item.mainimage.id == itemimg.id:
				itemimg.item.mainimage = None
				itemimg.item.save()
			itemimg.delete()
		return HttpResponse(700)
	return HttpResponse(500)

#The request contains the image id of the new main image
@login_required
def setmainimage(request):
	if request.method == "POST":
		imageid = request.POST['mainimageid']
		img = Image.objects.get(id=imageid)
		bu = BasicUser.objects.get(user = request.user)
		if img.item.user == bu:
			img.item.mainimage = img
			img.item.save()
		return HttpResponse(700)
	return HttpResponse(500)
	
# Save an uploaded image and send back the image icon for display
@login_required
def imageupload(request,itemid):
	try:
		if itemOwner(request,itemid):
			item = Item.objects.get(id=itemid)
			imagehandlers = []
			for file in request.FILES.getlist('files'):
				extension = file.name.split('.')[1]
				extension = extension.lower()
				if not (extension == 'png' or extension == 'jpg'):
					return HttpResponse(json.dumps('filetype'), content_type='application/json')
				if file.size > 1048576:
					return HttpResponse(json.dumps('filesize'), content_type='application/json')
				if item.image_set.count() > 10:
					return HttpResponse(json.dumps('filecount'), content_type='application/json')
				ui = Image(item=item,photo=file,photo_small=file,photo_medium=file)
				ui.save()
				imagehandlers.append([ui.id,ui.photo_medium.url])
			return HttpResponse(json.dumps(imagehandlers), content_type='application/json')
	except:
		return HttpResponse(json.dumps('error'), content_type='application/json')
	
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
			item.shippingincluded = True if request.POST.get('shippingincluded','True') == 'True' else False
			item.offlineviewing = True if request.POST.get('offlineviewing','True') == 'True' else False
			price = request.POST.get('inputlistprice','0')
			if price:
				new_price = int(round(float(price.replace(",","").replace("$","0")),2)*100)
				if item.price and item.price != new_price and item.liststatus == "active":
					pc = PriceChange(item=item,original_price=item.price,new_price=new_price)
					pc.save()
				item.price = new_price
			msrp_price = request.POST.get('inputmsrpprice','0')
			if msrp_price:
				item.msrp_price = int(round(float(msrp_price.replace(",","").replace("$","0")),2)*100)
			item.charity = True if request.POST.get('charity',False) else False
			item.charity_name = Charity.objects.get(name=request.POST.get('charity_name','Any'))
			item.save()
			return HttpResponse(submitcode)
		return HttpResponse(500)
	except Exception,e:
		print e
		return HttpResponse(500)
		
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
			item.tos = True
			item.save()
			email_view.composeEmailListingConfirmation(request,request.user.basicuser,item)
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
		bu = BasicUser.objects.get(user=request.user)
		if SavedItem.objects.filter(user=bu,item=item).exists():
			saved = True
		if item.user != bu:
			item.views += 1
			item.save()
		if BuyAuthorization.objects.filter(seller=item.user,item=item,buyer=bu).exists():
			authorized = True
	related = Item.objects.filter(subcategory = item.subcategory).filter(liststatus='active').order_by('views')[:9]
	dict = {'saved':saved,'item':item,'industry':industry,'related':related,'authorized':authorized}
	#Is the item in their shopping cart?
	isInShoppingCart = False
	if shoppingcart:
		for cartitem in shoppingcart.cartitem_set.all():
			if cartitem.item == item:
				isInShoppingCart = True
	dict['isinshoppingcart'] = isInShoppingCart
	return render_to_response('product/productdetails.html',dict,context_instance=RequestContext(request))

@login_required
def askquestion(request):
	if request.method == "POST" and request.user.is_authenticated():
		item = Item.objects.get(id=request.POST["itemid"])
		user = BasicUser.objects.get(user=request.user)
		redirect = request.POST["redirect"]
		question = request.POST['question']
		if len(question) > 3: # Make sure it is a legitimate question
			questionobject = Question(question=question,item=item,buyer=user,seller=item.user,dateanswered=None,answer='')
			questionobject.save() 
			email_view.composeEmailNewQuestion(request,user,questionobject)
		return HttpResponseRedirect(redirect)
	return HttpResponseRedirect("/login?next="+redirect)

def deletequestion(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = request.user.basicuser
		questionid = request.POST['questionid']
		page = request.POST.get('questionspage','')
		ques = Question.objects.get(id=questionid)
		if ques.buyer == bu or ques.seller == bu:
			ques.delete()
	if not page:
		return HttpResponse(json.dumps(201), content_type='application/json')
	else:
		return HttpResponseRedirect("/account/sellerquestions")
		
###########################################
#### User Function Pages ##################
###########################################

def existingproductcheck(request):
	if request.method == "GET":
		subcategory = request.GET['category']
		products = Product.objects.get(name=subcategory)
		for pnames in products:
			product_names.append(pnames.name)
		return HttpResponse(json.dumps({'products':product_names}), content_type='application/json')


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
		return HttpResponse(json.dumps({'status':"100"}), content_type='application/json')
	else:
		redirectURL = str('/login?next=/item/'+str(item.id)+"/details&action=save")
		return HttpResponse(json.dumps({'status':"400",'redirect':redirectURL}), content_type='application/json')

@login_required
def removeitem(request):
	if request.method == "POST" and request.user.is_authenticated():
		item = Item.objects.get(id=int(request.POST['itemid']))
		si = SavedItem.objects.get(user = BasicUser.objects.get(user=request.user),item=item)
		si.delete()
		return HttpResponseRedirect("/account/wishlist")
	return render_to_response('general/index.html',context_instance=RequestContext(request))

#### Checks if a request's user is the creator of the item
def itemOwner(request,itemid):
	try:
		bu = BasicUser.objects.get(user=request.user)
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