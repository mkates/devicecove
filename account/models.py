from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import uuid, os
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField

def create_basic_user_image_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid.uuid4()), ext)
	return os.path.join('profileimages', filename)

############################################
####### User Class #########################
############################################	
# Generic User already includes email/password
class BasicUser(models.Model):
	# General
	user = models.OneToOneField(User)
	referrer = models.ForeignKey('self',null=True,blank=True) # Tracks the user who referred them
	referral_id = models.CharField(max_length=100) # The user's referral ID
	creation_date = models.DateTimeField(auto_now_add=True)
	
	firstname = models.CharField(max_length=60)
	lastname = models.CharField(max_length=60)
	email = models.EmailField(max_length=60) # Contact Email, login email stored in User class
	zipcode = models.CharField(max_length=20)

	# These automatically populate from the zipcode (store for speed purposes)
	city = models.CharField(max_length=100,blank=True)
	county = models.CharField(max_length=100,blank=True)
	state = models.CharField(max_length=100,blank=True)
	
	# Additional Business Information (if they are a seller)
	businesstype = models.CharField(max_length=60,blank=True)
	company = models.CharField(max_length=60,blank=True)
	website = models.CharField(max_length=60,blank=True)
	phonenumber = models.BigIntegerField(max_length=10,null=True,blank=True)
	mainimage = ProcessedImageField(upload_to=create_basic_user_image_path, processors=[ResizeToFit(300, 150)],format='JPEG',options={'quality': 60},null=True,blank=True) 

	# User's Rank (will be used for different commission classes, listing limits, etc.)
	USER_TYPE =  (('basic', 'basic'),('preferred','preferred'),('pharma', 'pharma'))
	user_type = models.CharField(max_length=2,choices=USER_TYPE,default='basic')

	# Current credit balance
	credits = models.BigIntegerField(max_length=10,default=0) # Stored for speed purposes

	# Payments
	balanceduri = models.CharField(max_length=255,blank=True)
	payment_method = models.ForeignKey('payment.Payment',related_name="paymentmethod",null=True,blank=True)
	payout_method = models.ForeignKey('payment.Payment',related_name="payoutmethod",null=True,blank=True)
	
	# Settings 
	newsletter = models.BooleanField(default=True)

	def name(self):
		return self.firstname+" "+self.lastname

	def __unicode__(self):
		return self.firstname+" "+self.lastname
		
	# Get number of unanswered questions
	def unansweredQuestionCount(self):
		return self.questionseller.filter(answer = "").count()
		
	# Number of asked questions
	def askedQuestionCount(self):
		return self.questionbuyer.count()
		
	# Number of items in wishlist
	def wishlist(self):
		return self.saveditem_set.count()
	
	#Get counts for each type of listing (used in profile page)
	# 'all' and 'inactive' are cumulative counts
	def listedItemCount(self):
		dict = {'all':0,'inactive':0,'sold':0,'unsold':0,'active':0,'incomplete':0,'disabled':0}
		for item in self.item_set.all():
			dict[item.liststatus] += 1
			if item.liststatus != 'disabled':
				dict['all'] += 1
			if item.liststatus == 'sold' or item.liststatus == 'unsold':
				dict['inactive'] += 1
		return dict
	
	# Number of Purchases
	def buyhistory(self):
		return self.purchaseditembuyer.count()
	
	# Number of Sales
	def sellhistory(self):
		return self.purchaseditemseller.count()

	# IDs of the approved vendors
	def approvedVendors(self):
		vendor_ids = [vendor.id for vendor in BasicUser.objects.filter(user_type="basic")]
		for vendor in self.unapprovedvendoruser.all():
			vendor_ids.pop(vendor_ids.index(vendor.id))
		return vendor_ids

############################################
####### Approved Providers #################
############################################
class UnapprovedVendor(models.Model):
	user = models.ForeignKey(BasicUser,related_name="unapprovedvendoruser")
	vendor = models.ForeignKey(BasicUser,related_name="unapprovedvendorvendor")

############################################
####### Credits ############################
############################################
class Credit(models.Model):
	user = models.ForeignKey(BasicUser,related_name="credituser")
	amount = models.IntegerField(max_length=6)
	expires = models.DateTimeField()
	CREDIT_TYPES = (('referral','Friend Referral'),('signup','New Customer'),('sale','Sale'))
	credittype = models.CharField(max_length=2,choices=CREDIT_TYPES,default=0)
	referree = models.ForeignKey(BasicUser,related_name="creditreferree",null=True,blank=True)
	purchaseditem = models.ForeignKey('purchase.PurchasedItem',null=True,blank=True)

	def __unicode__(self):
		return self.credittype+ "Credit"

############################################
####### Wishlist Items #####################
############################################
class SavedItem(models.Model):
	user = models.ForeignKey(BasicUser)
	item = models.ForeignKey('listing.Item')

############################################
####### Addresses Model  ###################
############################################
class Address(models.Model):
	user = models.ForeignKey(BasicUser,null=True,blank=True)
	name = models.CharField(max_length=50) # full name
	address_one = models.CharField(max_length=100) #street address,p.o. box, company name c/o
	address_two = models.CharField(max_length=100,blank=True) #apartment, suite, unit, building,floor,etc.
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100) #Can be state/province/or region
	country = models.CharField(max_length=50, default="United States")
	zipcode = models.CharField(max_length=20) # Can be zipcode or postal code
	phonenumber = models.CharField(max_length=20) 

############################################
### Feedback ###############################
############################################
class Feedback(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(BasicUser)
	love = models.TextField()
	change = models.TextField()

############################################
####### Lat Long Model #####################
############################################
class LatLong(models.Model):
	zipcode = models.IntegerField(max_length=5, db_index=True,unique=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	county = models.CharField(max_length=50)

