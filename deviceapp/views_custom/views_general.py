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
from django.conf import settings
import json
import math
import difflib
import locale
import time


def index(request):
	items = Item.objects.order_by('savedcount')[:9]
	return render_to_response('general/index.html',{'featured':items},context_instance=RequestContext(request))

def categories(request):
	return render_to_response('general/categories.html',{'categories':Category.objects.all()},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('general/faqs.html',context_instance=RequestContext(request))

def testemail(request):
	return render_to_response('email_templates/test_email.html',context_instance=RequestContext(request))
	
def my_404_view(request):
	return render_to_response('404.html',context_instance=RequestContext(request))
	
def buyerprotect(request):
	return render_to_response('general/buyerprotect.html',context_instance=RequestContext(request))

### Anytime there is an error, send the user here ####
def error(request,errorname):
	errormessage = ''
	if errorname == 'notpost':
		errormessage = 'There was an invalid POST request'
	if errorname == 'signup':
		errormessage = 'There was an error signing up'
	return render_to_response('general/error.html',{'errormessage':errormessage},context_instance=RequestContext(request))

