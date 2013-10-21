from django.shortcuts import render_to_response
from deviceapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.utils import simplejson

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))
	
def search(request):
	return render_to_response('search.html',context_instance=RequestContext(request))

def loginview(request):
	try:
		next = request.GET['next']
	except:
		next = None
	return render_to_response('login.html',{'next':next},context_instance=RequestContext(request))

def signup(request):
	return render_to_response('signup.html',context_instance=RequestContext(request))


@login_required
def saveditems(request):
	return render_to_response('saveditems.html',context_instance=RequestContext(request))
@login_required
def listeditems(request):
	return render_to_response('listeditems.html',context_instance=RequestContext(request))
@login_required
def accounthistory(request):
	return render_to_response('accounthistory.html',context_instance=RequestContext(request))
@login_required
def settings(request):
	return render_to_response('settings.html',context_instance=RequestContext(request))
@login_required
def profile(request):
	return render_to_response('profile.html',context_instance=RequestContext(request))
@login_required
def addproduct(request):
	return render_to_response('addproduct.html',context_instance=RequestContext(request))


def forgotpassword(request):
	return render_to_response('passwordreset.html',context_instance=RequestContext(request))

def product(request):
	return render_to_response('product.html',context_instance=RequestContext(request))

def lgnrequest(request):
	username = request.POST['email']
	password = request.POST['password']
	user = authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			try:
				request.GET['next']
				return HttpResponseRedirect(request.GET['next'])
			except:
				return HttpResponseRedirect("/signup")
		else:
			return HttpResponse("Your account has been disabled")
	else:
		return render_to_response('login.html',{'outcome':'Invalid Login'},context_instance=RequestContext(request))
	
def newuserform(request):
	print "YEEAHW"
	
	if request.method == 'POST':
		try:
			businesstype = request.POST['businesstype']
			company = request.POST['company']
			name = request.POST['name']
			email = request.POST['email']
			address = request.POST['address']
			zipcode = request.POST['zipcode']
			city = request.POST['city']
			state = request.POST['state']
			website = request.POST['website']
			phonenumber = request.POST['phonenumber']
			password = request.POST['password']
			user = User.objects.create_user(email,email,password)
			user.save()
			nbu = BasicUser(user=user,businesstype=businesstype,company=company,email=email,address=address,zipcode=zipcode,city=city,
			state=state,website=website,phonenumber=phonenumber,password=password)
			nbu.save()
			return HttpResponse("Success")
		except Exception,e:
			return HttpResponse(e)
	return HttpResponse("Your account has been created")
	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

	