from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.conf import settings
import json, math, difflib, locale, time, string
from django.core.cache import cache
from general.models import *
from listing.models import *
from general.forms import *


#PDF GENERATION INPUT
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from django.contrib.auth.models import User
from django.templatetags.static import static
from reportlab.lib.pagesizes import letter,landscape
from io import BytesIO
import os.path

def pdf(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	# Optionally add a filname so it automatically downloads
	#response['Content-Disposition'] = 'attachment; filename="My Users.pdf"'

	#Create buffer
	buffer = BytesIO()
	pdf = print_users(buffer)

	response.write(pdf)
	return response

#PDF size is 612x792 pixels
def print_users(buffer):
	doc = SimpleDocTemplate(buffer,
	                        rightMargin=36,
	                        leftMargin=36,
	                        topMargin=80,
	                        bottomMargin=54,
	                        pagesize=(8.5*inch, 11*inch))

	# Our container for 'Flowable' objects
	elements = []

	# A large collection of style sheets pre-made for us
	styles = getSampleStyleSheet()

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	elements.append(Paragraph('My User Names', styles['Heading1']))
	numbers = ['cool' for i in range(10)]
	for user in numbers:
	    elements.append(Paragraph(user, styles['Normal']))
	# Need a place to store our table rows
	table_data = []
	for user in ['some really really really some really really reallysome really really really','b','c']:
		p = Paragraph("long line long line long line long line long line long line",styles['Normal'])
		table_data.append([p,p,p])
	# Create the table
	user_table = Table(table_data, colWidths=[doc.width/3.0]*3)
	user_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                                ('BOX', (0, 0), (-1, -1), 1, colors.black)]))
	user_table2 = Table(table_data, colWidths=[doc.width/3.0]*3)
	user_table2.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                                ('BOX', (0, 0), (-1, -1), 1, colors.black)]))
	elements.append(user_table2)
	elements.append(user_table2)
	doc.build(elements,onFirstPage=_header_footer, onLaterPages=_header_footer,canvasmaker=NumberedCanvas)

	# Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	return pdf

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Light', fontName='Helvetica',alignment=TA_CENTER,fontSize=6,leading=8,textColor=colors.Color(0,0,0,.5)))

    # Header
    #header = Paragraph('This is our obligatory message that we attach to the bottom of every one of our pages. This information is intended for the Veterinary Clinic.', styles['Normal'])

    # Background Image 
    img2 = Image('/Users/alexanderkates/Dropbox/WebProjects/medbay/medapp/static/img/pdf/pdfbackground.jpg',width=8.5*inch,height=11*inch)
    img2.drawOn(canvas,0,0)

    # Footer
    footer = Paragraph('This report was generated by Vetcove on August 25th, 2014. Information in this report is subject to change, and is strictly intended for the viewing by Colts Neck Equine. For more information, contact Vetcove directly at www.vetcove.com, via email at info@vetcove.com, or py phone at 732.598.6434', styles['Light'])
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h+20)

    # Release the canvas
    canvas.restoreState()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.setFont('Helvetica',8)
        self.drawCentredString(4* inch, 2.5 * mm + (0.0 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))















#############################################################
######## General Pages ######################################
#############################################################

### Manually view the browser upgrade page
def browserUpgrade(request):
	return render_to_response('general/ieupgrade.html',{},context_instance=RequestContext(request))

### Homepage ####
def index(request):
	# If the user is authenticated, show the appropriate homepage
	if request.user.is_authenticated():
		group_type = request.user.basicuser.group_type() 
		if group_type == 'supplier':
			return HttpResponseRedirect('/portal/dashboard')
		else:
			return HttpResponseRedirect('/dashboard')
	# If the user is not logged in, render the generic page
	else:
		return render_to_response('general/index.html',{},context_instance=RequestContext(request))

### Category Directory ###
def categories(request):
	categories = Category.objects.all().prefetch_related('parent').order_by('displayname')
	maincategories = categories.filter(main=True).order_by('displayname')
	for maincat in maincategories:
	 	maincat.subcategories = [subcat for subcat in categories if subcat.parent == maincat]
	return render_to_response('general/categories.html',{'pagecategories':maincategories},context_instance=RequestContext(request))

### Referral Landing Page ###
def newReferral(request,referral_id):
	request.session['referral_id'] = referral_id
	return render_to_response('general/index.html',{},context_instance=RequestContext(request))

#############################################################
######## Corporate Pages ####################################
#############################################################

### Features for Veterinarians ###
def features(request):
	return render_to_response('general/corporate/features.html',{'learn_features':True},context_instance=RequestContext(request))

### Features for Manufacturer ###
def manufacturer(request):
	return render_to_response('general/corporate/manufacturer.html',{'learn_manufacturer':True},context_instance=RequestContext(request))

### Features for Distributor ###
def supplier(request):
	return render_to_response('general/corporate/supplier.html',{'learn_supplier':True},context_instance=RequestContext(request))

#############################################################
######## Information Pages ##################################
#############################################################

def tos(request):
	return render_to_response('general/information/tos.html',{'tos':True},context_instance=RequestContext(request))

def giveback(request):
	return render_to_response('general/information/giveback.html',{'giveback':True},context_instance=RequestContext(request))

def pricing(request):
	return render_to_response('general/information/pricing.html',{'pricing':True},context_instance=RequestContext(request))

def rewards(request):
	return render_to_response('general/information/rewards.html',{'rewards':True},context_instance=RequestContext(request))

def privacypolicy(request):
	return render_to_response('general/information/privacypolicy.html',{'privacypolicy':True},context_instance=RequestContext(request))

def faq(request):
	return render_to_response('general/information/faqs.html',{'faq':True},context_instance=RequestContext(request))

def about(request):
	return render_to_response('general/information/about.html',{'about':True},context_instance=RequestContext(request))

def buyerprotect(request):
	return render_to_response('general/information/buyerprotect.html',{'buyerprotect':True,'PHONE_NUMBER':settings.CONTACT_PHONE_NUMBER},context_instance=RequestContext(request))

#############################################################
######## Contact ############################################
#############################################################

def contact(request):
	return render_to_response('general/information/contact.html',{'contact':True},context_instance=RequestContext(request))

def contactform(request):
	form = ContactForm(request.POST)
	if form.is_valid():		
		# General user sign-up
		name = form.cleaned_data['name']
		email = form.cleaned_data['email']
		message = form.cleaned_data['message']
		user = None
		if request.user.is_authenticated():
			user = request.user.basicuser
		cf = Contact(user=user,name=name,email=email,message=message)
		cf.save()
		email_view.composeContactForm(cf)
		return render_to_response('general/contact.html',{'contact':True,'success':True},context_instance=RequestContext(request))	
	return render_to_response('general/contact.html',{'contact':True,'failure':True},context_instance=RequestContext(request))

#############################################################
######## Error Pages ########################################
#############################################################

def my_404_view(request):
	print 'here'
	return render_to_response('error/404.html',context_instance=RequestContext(request))

def my_500_view(request):
	return render_to_response('error/500.html',context_instance=RequestContext(request))

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

	
	