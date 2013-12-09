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


def index(request):
	items = Item.objects.order_by('savedcount')[:9]
	return render_to_response('index.html',{'featured':items},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('faqs.html',context_instance=RequestContext(request))

def buyerprotect(request):
	return render_to_response('buyerprotect.html',context_instance=RequestContext(request))

def listintro(request):
	manufacturer = Manufacturer.objects.all()
	category = DeviceCategory.objects.all().extra(order_by = ['displayname'])
	return render_to_response('listintro.html',{'manufacturer':manufacturer,'category':category},context_instance=RequestContext(request))