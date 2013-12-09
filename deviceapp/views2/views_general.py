from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
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


def index(request):
	items = Item.objects.order_by('savedcount')[:9]
	return render_to_response('index.html',{'featured':items},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('faqs.html',context_instance=RequestContext(request))

def my_404_view(request):
	return render_to_response('404.html',context_instance=RequestContext(request))
	
def buyerprotect(request):
	return render_to_response('buyerprotect.html',context_instance=RequestContext(request))

def listintro(request):
	category = Category.objects.all().extra(order_by = ['displayname'])
	dict = []
	for cat in category:
		dict.append([cat,cat.subcategory_set.all()])
	return render_to_response('listintro.html',{'categories':category},context_instance=RequestContext(request))

def getsubcategories(request):
	category = Category.objects.get(name=request.GET['category'])
	subcategories = SubCategory.objects.filter(category=category)
	dict = {}
	for sub in subcategories:
		dict[sub.name] = sub.displayname
	return HttpResponse(json.dumps(dict), mimetype='application/json')

