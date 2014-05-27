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
	
############################################
####### The Basic User Object ##############
############################################
class BasicUser(models.Model):
	user = models.OneToOneField(User)
	creation_date = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	member = models.ForeignKey('Basic',null=True,blank=True)

### General Information Pertaining To All User Types On Our System ###
class Basic(models.Model):
	### General Modification Data ###
	creation_date = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)

	email = models.EmailField(max_length=60) #Added automatically, editable
	address = models.ForeignKey('Address',related_name="main_address",null=True,blank=True)
	phonenumber = models.CharField(max_length=20,null=True,blank=True)
	### Referral Information ###
	referrer_id = models.CharField(max_length=8) # The ID used to give out referrals
	referrer_user = models.ForeignKey('self',null=True,blank=True) # Did another clinic refer them to join?, lets store it

	### Payments ###
	balanceduri = models.CharField(max_length=255,blank=True,null=True)
	payment_method = models.ForeignKey('payment.Payment',null=True,blank=True,related_name='basic_payment_method')
	payout_method = models.ForeignKey('payment.Payment',null=True,blank=True,related_name='basic_payout_method')

	# Current credit balance
	credits = models.BigIntegerField(max_length=12,default=0) # Stored for speed purposes

	# # Override the default creation to add a referral ID to each user
	# def save(self, *args, **kwargs):
	# 	if not self.pk: # Only on creation save
	# 		self.referrer_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
	# 	super(Basic,self).save(*args, **kwargs)

	def handle(self):
		return self.supplier if hasattr(self,'supplier') else (self.clinic if hasattr(self,'clinic') else self.individual)

	def type(self):
		return 'supplier' if hasattr(self,'supplier') else ('clinic' if hasattr(self,'clinic') else 'individual')

class Individual(Basic):
	clinic=models.ForeignKey('Clinic',null=True,blank=True)

class Company(Basic):
	### Personal Information ###
	company_name = models.CharField(max_length=60)
	website = models.CharField(max_length=60,blank=True,null=True)
	mainimage = ProcessedImageField(upload_to=create_company_image_path, processors=[ResizeToFit(300, 150)],format='JPEG',options={'quality': 60},null=True,blank=True) 

	class Meta:
		abstract=True

############################################
####### Clinic #############################
############################################	
class Clinic(Company):
	### Security Credentials###
	practitioner_name= models.CharField(max_length=60)
	approved_until = models.DateField(blank=True,null=True)
	license = ProcessedImageField(upload_to=create_license_path,format='JPEG',options={'quality': 60},null=True,blank=True) 
	license_expiration = models.DateField(null=True,blank=True)
	license_state = models.CharField(max_length=60,null=True,blank=True)
	
	### Practice Type ###
	small_animal = models.BooleanField(default=False)
	large_animal = models.BooleanField(default=False)
	equine = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.company_name

	# Number of items in wishlist
	def savedcount(self):
		return self.saveditem_set.count()

	def listedItemCount(self):
		dict = {'all':0,'inactive':0,'sold':0,'unsold':0,'active':0,'incomplete':0,'disabled':0}
		for item in self.item_set.all():
			dict[item.liststatus] += 1
			if item.liststatus != 'disabled':
				dict['all'] += 1
			if item.liststatus == 'sold' or item.liststatus == 'unsold':
				dict['inactive'] += 1
		return dict

############################################
####### Supplier ###########################
############################################
class Supplier(Company):
	description = models.TextField()
	sell_scripts = models.BooleanField(default=False)
	can_sell_rx = models.BooleanField(default=False)

	def __unicode__(self):
		return self.company_name



### Names of All the GPOs ###
class GPO(models.Model):
	name = models.CharField(max_length=50,unique=True)
	clinics = models.ManyToManyField(Clinic)



############################################
####### Credits ############################
############################################
class Credit(models.Model):
	basic = models.ForeignKey(Basic)
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
	basic = models.ForeignKey(Basic,null=True,blank=True,related_name="address_clinic")
	name = models.CharField(max_length=50) # full name
	address_one = models.CharField(max_length=100) # street address,p.o. box, company name c/o
	address_two = models.CharField(max_length=100,blank=True,null=True) # apartment, suite, unit, building,floor,etc.
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100) #Can be state/province/or region
	country = models.CharField(max_length=50, default="United States")
	zipcode = models.CharField(max_length=20) # Can be zipcode or postal code, i.e. in Canada its A2E4D9


