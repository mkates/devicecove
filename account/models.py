from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import uuid, os, random, string
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField

def create_company_image_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid.uuid4()), ext)
	return os.path.join('companyimages', filename)

def create_license_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid.uuid4()), ext)
	return os.path.join('license', filename)

def create_sales_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid.uuid4()), ext)
	return os.path.join('sales', filename)

############################################
####### The Basic User Object ##############
############################################
class BasicUser(models.Model):
	user = models.OneToOneField(User)
	creation_date = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	### Points to the parent group class, which can be a clinic, supplier, individual, etc. ###
	group = models.ForeignKey('Group',blank=True,null=True)
	
	def __unicode__(self):
		return self.user.username

	# Returns a handle of the group, 'clinic','supplier','group'
	def group_handle(self):
		return self.group.group_handle()

	# Returns a string of the type of group, 'clinic','supplier','other'
	def group_type(self):
		return self.group.group_type()

### General Information Pertaining To All User Types ###
class Group(models.Model):
	### General Modification Data ###
	creation_date = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)

	### Contact Information ###
	email = models.EmailField(max_length=60) #Added automatically, editable
	address = models.ForeignKey('Address',related_name="main_address",null=True,blank=True)
	phonenumber = models.CharField(max_length=20,null=True,blank=True)
	
	### Referral Information ###
	referrer_id = models.CharField(max_length=10) # The ID used to give out referrals
	referrer_user = models.ForeignKey('self',null=True,blank=True) # Did another clinic refer them to join?, lets store it

	### Payments ###
	balanceduri = models.CharField(max_length=255,blank=True,null=True)
	payment_method = models.ForeignKey('payment.Payment',null=True,blank=True,related_name='basic_payment_method')
	payout_method = models.ForeignKey('payment.Payment',null=True,blank=True,related_name='basic_payout_method')
	
	# Current credit balance
	credits = models.BigIntegerField(max_length=12,default=0) # For buyers (rewards) and sellers (discounts on promotions)

	def group_handle(self):
		if hasattr(self,'clinic'):
			return self.clinic
		elif hasattr(self,'supplier'):
			return self.supplier
		else:
			return None

	def group_type(self):
		if hasattr(self,'clinic'):
			return 'clinic'
		elif hasattr(self,'supplier'):
			return 'supplier'
		else:
			return 'other'

############################################
####### Clinic #############################
############################################	
class Clinic(Group):
	### Basic Information ###
	name = models.CharField(max_length=60,blank=True,null=True)
	practitioner_name= models.CharField(max_length=60,blank=True,null=True)
	license_no = models.CharField(max_length=60,blank=True,null=True)
	state = models.CharField(max_length=60,null=True,blank=True)
	license = ProcessedImageField(upload_to=create_license_path,format='JPEG',options={'quality': 60},null=True,blank=True)
	license_expiration = models.DateField(null=True,blank=True)
	sales_no = models.CharField(max_length=60,null=True,blank=True)
	sales = models.FileField(upload_to=create_sales_path,null=True,blank=True)
	
	### Details ###
	organization_type = models.CharField(max_length=100,null=True,blank=True)
	number_of_vets = models.PositiveIntegerField(default=1)
	practice_size = models.PositiveIntegerField(default=1)
	website = models.CharField(max_length=60,blank=True,null=True)
	PRACTICE_TYPES = (('small_animal','Small Animal'),('large_animal','Large Animal'),('mixed','Mixed'))
	practice_type = models.CharField(max_length=60,choices=PRACTICE_TYPES,null=True,blank=True,default='')
	
	tos = models.BooleanField(default=False) # Did they agree to the TOS?


	verified = models.BooleanField(default=False) # Are they eligible to purchase on our system?
	
	def __unicode__(self):
		return self.name

	# Number of items in wishlist
	def savedcount(self):
		return self.saveditem_set.count()

############################################
####### Supplier ###########################
############################################
class Supplier(Group):
	### Basic Information From Initial Form ###
	name = models.CharField(max_length=50,unique=True,null=True,blank=True)
	primary_contact = models.CharField(max_length=100,null=True,blank=True)
	website = models.CharField(max_length=100,null=True,blank=True)
	current_selling_method = models.CharField(max_length=100,null=True,blank=True)
	interest_listings = models.BooleanField(default=False)
	interest_community = models.BooleanField(default=False)
	interest_promotions = models.BooleanField(default=False)
	interest_direct = models.BooleanField(default=False)
	product_size = models.CharField(max_length=100,null=True,blank=True)
	referral_source = models.CharField(max_length=100,null=True,blank=True)
	application_submitted = models.BooleanField(default=False) # Did they submit the new supplier form? #
	
	### Seconday Information ###
	# logo_field
	description = models.TextField()
	can_sell_rx = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name


### Names of All the GPOs ###
class GPO(models.Model):
	name = models.CharField(max_length=50,unique=True)
	clinics = models.ManyToManyField(Clinic)

############################################
####### Credits ############################
############################################
class Credit(models.Model):
	basic = models.ForeignKey(Group)
	amount = models.BigIntegerField(max_length=12) # In cents
	CREDIT_TYPES = (('referral','Friend Referral'),('signup','New Customer'),('promotion','Promotion'),('sale','sale'))
	credittype = models.CharField(max_length=2,choices=CREDIT_TYPES,default=0)
	referree = models.ForeignKey(BasicUser,related_name="creditreferree",null=True,blank=True)
	purchaseditem = models.ForeignKey('purchase.PurchasedItem',null=True,blank=True)

	def __unicode__(self):
		return self.credittype+ "Credit"

############################################
####### Wishlist Items #####################
############################################
class SavedItem(models.Model):
	clinic = models.ForeignKey(Clinic)
	item = models.ForeignKey('listing.Product')

############################################
####### Addresses Model  ###################
############################################
class Address(models.Model):
	group = models.ForeignKey(Group,null=True,blank=True,related_name="address_clinic")
	name = models.CharField(max_length=50) # full name
	address_one = models.CharField(max_length=100) # street address,p.o. box, company name c/o
	address_two = models.CharField(max_length=100,blank=True,null=True) # apartment, suite, unit, building,floor,etc.
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100) #Can be state/province/or region
	country = models.CharField(max_length=50, default="United States")
	zipcode = models.CharField(max_length=20) # Can be zipcode or postal code, i.e. in Canada its A2E4D9


