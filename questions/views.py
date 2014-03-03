from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from questions.models import *
from deviceapp.models import *
import emails.views as email_view
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.timezone import utc
import json,locale 
from datetime import datetime

############################################
########## Questions #######################
############################################


### Questions for the seller page ###
@login_required
def sellerquestions(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)	
		questions = Question.objects.filter(seller=bu)
		answered = []
		unanswered = []
		for question in questions:
			if question.answer:
				answered.append(question)
			else:
				unanswered.append(question)
		return render_to_response('account/questions/sellerquestions.html',{'answered':answered,'unanswered':unanswered},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

### Questions for the buyer page ###
@login_required
def buyerquestions(request):
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)	
		questions = Question.objects.filter(buyer=bu)
		return render_to_response('account/questions/buyerquestions.html',{'questions':questions},context_instance=RequestContext(request))
	else:
   		return render_to_response('general/index.html',context_instance=RequestContext(request))

### When a buyer asks a question ###
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
			notification = SellerQuestionNotification(user=item.user,question=questionobject)
			notification.save()
			email_view.composeEmailNewQuestion(user,questionobject)
		return HttpResponseRedirect(redirect)
	return HttpResponseRedirect("/login?next="+redirect)

### When a buyer/seller deletes a question ###
def deletequestion(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = request.user.basicuser
		questionid = request.POST['questionid']
		page = request.POST.get('questionspage','') # Original page
		ques = Question.objects.get(id=questionid)
		if ques.buyer == bu or ques.seller == bu:
			ques.delete()
		if not page:
			return HttpResponse(json.dumps(201), content_type='application/json')
	else:
		return HttpResponseRedirect("/account/sellerquestions")
		
### When a seller answers a question ###
@login_required
def answerquestion(request,questionid):
	if request.user.is_authenticated() and request.method == "POST":
		bu = BasicUser.objects.get(user=request.user)
		question = Question.objects.get(id=questionid)
		if question.item.user.id == bu.id:
			question.answer = request.POST.get('answer','')
			question.dateanswered = datetime.utcnow().replace(tzinfo=utc)
			question.save()
			# Create notification for buyer
			notification = BuyerQuestionNotification(user=question.buyer,question=question)
			notification.save()
			# Creat email for buyer
			email_view.composeEmailQuestionAnswered(question)
		return HttpResponseRedirect('/account/sellerquestions')
	return HttpResponseRedirect('/')