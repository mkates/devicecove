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
from django.conf import settings
import medapp.settings as settings
import json

def messageseller(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = BasicUser.objects.get(user=request.user)
		message = request.POST['message']
		seller = request.POST['seller']
		seller = BasicUser.objects.get(id=seller)
		selleremail = seller.email
		try:
			# SENDMAIL TO 
			print selleremail
			print message
			status = 200 #Success
		except:
			status = 500 #Error sending email
	else:
		status = 400 #User not logged in or method is not post
	return HttpResponse(json.dumps(status), mimetype='application/json')

def deletequestion(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = BasicUser.objects.get(user=request.user)
		questionid = request.POST['questionid']
		ques = Question.objects.get(id=questionid)
		ques.delete()
		status = 400
	else:
		status = 500
	return HttpResponse(json.dumps(status), mimetype='application/json')