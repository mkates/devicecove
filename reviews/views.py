from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.timezone import utc
import json, math, difflib, locale, time, re, string
from datetime import datetime
from helper.model_imports import *
from review.forms import *


##############################################
####### Reviews App ##########################
##############################################

### When a user posts a review on a product ###
@login_required
def postReview(request):
	if request.method == "POST":
		product = request.POST.get('product','')
		rating = request.POST.get('rating',3)
		review_text = request.POST.get('review','')
		reviewer = request.POST.get('reviewer','Anonymous')
		### Did they review the product before? ###
		purchased_items = PurchasedItems.objects.filter(item__in=product.item_set.all())
		item = purchased_items[0] if purchased_items else None
		review = Review(product=product,
						clinic=request.user.basicuser.clinic,
						rating = rating,
						review=review_text,
						anonymous=anonymous,
						item=item,
						item_quantity=purchased_items.count())
		review.save()
		return HttpResponse(json.dumps({'status':201,'review':generateReviewDictionary(review)}), content_type='application/json')
	return HttpResponse(json.dumps({'status':500}), content_type='application/json')

### When a user upvotes a review ###
@login_required
def upvoteReview(request):
	if request.method == "POST":
		review = Review.objects.get(id=request.POST.get('review',''))
		upvote = Upvote(clinic=request.user.basicuser.clinic,
						review=review)
		upvote.save()
		return HttpResponse(json.dumps({'status':201}), content_type='application/json')
	return HttpResponse(json.dumps({'status':500}), content_type='application/json')

### Generates a dictionary to pass back in json for a recently created review ###
def generateReviewDictionary(review):
	return {'product':review.product,'rating':review.rating*10,'text':review.review,
		'anonymous':anonymous,'item':item,'item_quantity':item_quantity,'reviewer':reviewer}
