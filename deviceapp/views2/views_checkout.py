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

def checkoutSignin(request,itemid):
	return render_to_response('checkout/checkout_login.html',{},context_instance=RequestContext(request))

def checkoutShipping(request,itemid):
	return render_to_response('checkout/checkout_shipping.html',{},context_instance=RequestContext(request))

def checkoutPayment(request,itemid):
	return render_to_response('checkout/checkout_payment.html',{},context_instance=RequestContext(request))

def checkoutReview(request,itemid):
	return render_to_response('checkout/checkout_review.html',{},context_instance=RequestContext(request))

def checkoutConfirmation(request,itemid):
	return render_to_response('checkout/checkout_confirmation.html',{},context_instance=RequestContext(request))


####################################################
###### Checkout Helper Methods #####################
####################################################

