from django.shortcuts import render_to_response
from deviceapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import render
from django.utils import simplejson

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))
	
def search(request):
	return render_to_response('search.html',context_instance=RequestContext(request))

