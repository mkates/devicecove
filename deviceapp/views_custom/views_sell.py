from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
import views_checkout as checkout_view
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
import balanced

@login_required
def messageseller(request,itemid):
	if request.user.is_authenticated() and request.method=="POST":
		item = Item.objects.get(id=itemid)
		bu = request.user.basicuser
		name = request.POST.get('contact-name','')
		email = request.POST.get('contact-email','')
		phone = request.POST.get('contact-phone','')
		reason = request.POST.get('contact-reason','')
		message = request.POST.get('contact-message','')
		seller = item.user
		sm = SellerMessage(buyer=bu,name=name,item=item,email=email,phone=phone,reason=reason,message=message) 
		sm.save()
		############################
		#### Send Email Here As Well
		############################
		status = 201
	else:
		status = 500
	return HttpResponse(json.dumps(status), content_type='application/json')

@login_required
def buyermessages(request,itemid):
	item = Item.objects.get(id=itemid)
	# If the user logged in owns the item
	if request.user.basicuser == item.user:
		if item.commission_paid:	
			return render_to_response('account/selling/messages.html',{'item':item},context_instance=RequestContext(request))
		else:
			return render_to_response('account/contact_gate.html',{'item':item},context_instance=RequestContext(request))


#################################################
### Gateway for viewing buyer interest  #########
#################################################
@login_required
def contact_gate(request,itemid):
	item = Item.objects.get(id=itemid)
	return render_to_response('account/contact_gate.html',{'gate':True,'item':item},context_instance=RequestContext(request))

# Calls the balanced create card, which adds the card to the user and sets default credit card
@login_required
def newcard_chargecommission(request,itemid):
	item = Item.objects.get(id=itemid)
	balanced_addCard = checkout_view.addBalancedCard(request)
	if balanced_addCard['status'] != 201:
		return HttpResponse(json.dumps({'status':balanced_addCard['status'],'error':balanced_addCard['error']}), content_type='application/json')	
	try:
		card = balanced_addCard['card']
		bu = request.user.basicuser
		card_uri = card.card_uri
		balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
		customer = balanced.Customer.find(bu.balanceduri)
		amount = int(item.price*.09*100)
		customer.debit(appears_on_statement_as="Vet Cove Fee",amount=amount,source_uri=card_uri)
		item.commission_paid = True
		item.save()
		return HttpResponse(json.dumps({'status':201}), content_type='application/json')
	except:
		return HttpResponse(json.dumps({'status':501,'error':'card_charge'}), content_type='application/json')


def deletequestion(request):
	if request.user.is_authenticated() and request.method=="POST":
		bu = request.user.basicuser
		questionid = request.POST['questionid']
		page = request.POST.get('questionspage','')
		ques = Question.objects.get(id=questionid)
		if ques.buyer == bu or ques.seller == bu:
			ques.delete()
	if not page:
		return HttpResponse(json.dumps(500), content_type='application/json')
	else:
		return HttpResponseRedirect("/questions")