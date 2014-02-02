from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from deviceapp.models import *
from django.template import RequestContext, Context, loader
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import commission as commission
import json
import math
import difflib
import locale
import time


def index(request):
	items = Item.objects.filter(liststatus='active').order_by('savedcount')[:9]
	return render_to_response('general/index.html',{'featured':items},context_instance=RequestContext(request))

def buy(request):
	return HttpResponseRedirect('/productsearch/veterinary/all/all')
	
def categories(request):
	categories = Category.objects.all().order_by('name')
	return render_to_response('general/categories.html',{'categories':categories},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('general/faqs.html',context_instance=RequestContext(request))

def pvp(request):
	return render_to_response('general/pvp.html',context_instance=RequestContext(request))

def about(request):
	return render_to_response('general/about.html',context_instance=RequestContext(request))

def testemail(request):
	return render_to_response('email_templates/test_email.html',context_instance=RequestContext(request))
	
def my_404_view(request):
	return render_to_response('404.html',context_instance=RequestContext(request))

def my_500_view(request):
	return render_to_response('500.html',context_instance=RequestContext(request))
	
def buyerprotect(request):
	return render_to_response('general/buyerprotect.html',context_instance=RequestContext(request))

### Anytime there is an error, send the user here ####
def error(request,errorname):
	errormessage = ''
	if errorname == 'notpost':
		errormessage = 'There was an invalid POST request'
	if errorname == 'signup':
		errormessage = 'There was an error signing up'
	if errorname == 'itemdoesnotexist':
		errormessage = 'This item has been taken down or sold'
	return render_to_response('general/error.html',{'errormessage':errormessage},context_instance=RequestContext(request))

@login_required
def staffOverviewForward(request):
	return HttpResponseRedirect('/staff/overview/dashboard')
	
@staff_member_required
def staffOverview(request,type):
	if request.user.is_staff and request.user.is_authenticated():
		dict = {}
		if type == 'dashboard':
			# Get relevant objects
			pi = PurchasedItem.objects.all()
			users = BasicUser.objects.all().count()
			active_items = Item.objects.filter(liststatus="active").count()
			checkouts = Checkout.objects.filter(purchased=True).count()
			bp = BankPayout.objects.all()
			cp = CheckPayout.objects.all()
			
			total_amount_charged = 0
			number_items_sold = 0
			online_commission_revenue = 0
			for p in pi:
				total_amount_charged += p.quantity*p.unit_price
				number_items_sold += p.quantity
				if not p.cartitem.item.commission_paid:
					online_commission_revenue += commission.purchaseditemCommission(p)

			offline_commission_revenue = 0
			total_paidout = 0
			total_ccfee_revenue = 0
			for b in bp:
				total_paidout += b.amount
				total_ccfee_revenue += b.cc_fee
			for c in cp:
				total_paidout += c.amount
				total_ccfee_revenue += c.cc_fee
			for comm in Commission.objects.all():
				offline_commission_revenue += comm.amount
				
			total_commission_revenue = online_commission_revenue + offline_commission_revenue
			tobepaidout = total_amount_charged-total_paidout-total_commission_revenue-total_ccfee_revenue
			total_revenue = total_commission_revenue+total_ccfee_revenue
			dict = {'dashboard':True,'users':users,'checkouts':checkouts,'items_sold':number_items_sold,
			'offline_commission_revenue':offline_commission_revenue,'amount_sold':total_amount_charged,
			'total_paidout':total_paidout,'active_items':active_items, 'tobepaidout':tobepaidout,
			'online_commission_revenue':online_commission_revenue,
			'total_commission_revenue':total_commission_revenue,
			'total_revenue':total_revenue}
		elif type == 'purchaseditem':
			dict['purchaseditems'] = PurchasedItem.objects.all()
		elif type == 'bankpayout':
			dict['bankpayout'] = BankPayout.objects.all()
		elif type == 'checkpayout':
			dict['checkpayout'] = CheckPayout.objects.all()
		elif type == 'commission':
			dict['commission'] = Commission.objects.all()
			print 'here'
			print dict['commission']
		return render_to_response('general/adminoverview.html',dict,context_instance=RequestContext(request))
	return HttpResponseRedirect("/")

@staff_member_required
def staffMarkAsSent(request):
	if request.user.is_staff and request.user.is_authenticated() and request.method=="POST":
		cpid = request.POST.get('cp_id','')
		cpval = request.POST.get('cp_val','')
		cp = CheckPayout.objects.get(id=cpid)
		if cpval == 'sent':
			cp.sent = False
		else:
			cp.sent = True
		cp.save()
		return HttpResponse(json.dumps({'status':201,'sent':cp.sent}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({'status':500}), content_type='application/json')
	
	
	
	
	
	