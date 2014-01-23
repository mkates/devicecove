from django.shortcuts import render_to_response, redirect, render
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

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


def sendwelcomeemail(request):
	template_data = {'email_pagetitle':'VetCove',
			'email_teaser':'Welcome to VetCove. The worlds largest online equipment marketplace',
			'email_header':'Welcome to VetCove!',
			'STATIC_URL':settings.STATIC_URL}
	subject = "Welcome to VetCove!"
	plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
	text_body = render_to_string("email_templates/test_plain.txt", template_data, plaintext_context)
	html_body = render_to_string("email_templates/test_email2.html", template_data)
	msg = EmailMultiAlternatives(subject=subject, from_email="mhkates@gmail.com",to=["mkates@mit.edu"], body=text_body)
	msg.attach_alternative(html_body, "text/html")
	#msg.send()
	return

def testmail(request):
	question = Question.objects.get(id=1)
	template_data = {'question':question,
			'email_title':'VetCove',
			'email_teaser':'Welcome to VetCove. The worlds largest online equipment marketplace',
			'email_header':'Welcome to VetCove!',
			'STATIC_URL':settings.STATIC_URL,
			'email_name':'Alex Kates'}
	subject = "Welcome to VetCove!"
	plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
	text_body = render_to_string("email_templates/test_plain.txt", template_data, plaintext_context)
	html_body = render_to_string("email_templates/email_base.html", template_data)
	msg = EmailMultiAlternatives(subject=subject, from_email="mhkates@gmail.com",to=["mkates@mit.edu"], body=text_body)
	msg.attach_alternative(html_body, "text/html")
	msg.send()
	return render_to_response('email_templates/email_base.html',template_data,context_instance=RequestContext(request))

