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

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


def sendwelcomeemail(request):
	template_data = {'Name': "Joe", 'Email': "mhkates@gmail.com"}

	plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
	subject = "Welcome to VetCove"
	text_body = render_to_string("email_templates/test_plain.txt", template_data, plaintext_context)
	html_body = render_to_string("email_templates/test_email.html", template_data)
	msg = EmailMultiAlternatives(subject=subject, from_email="mhkates@gmail.com",to=["mkates@mit.edu"], body=text_body)
	msg.attach_alternative(html_body, "text/html")
	msg.send()
	return