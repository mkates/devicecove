from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import uuid, os
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField

def create_company_image_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid.uuid4()), ext)
	return os.path.join('companyimages', filename)

############################################
####### User ###############################
############################################
class BasicUser(models.Model):
	user = models.OneToOneField(User)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)

############################################
####### Clinic #############################
############################################	
class Clinic(models.Model):
	members = models.ManyToManyField(BasicUser)
	referrer = models.ForeignKey('self',null=True,blank=True) # Tracks the user who referred them
	referral_id = models.CharField(max_length=100) # The user's referral ID
	creation_date = models.DateTimeField(auto_now_add=True)

	business_name = models.CharField(max_length=60)
	businesstype = models.CharField(max_length=60,blank=True)
	company = models.CharField(max_length=60,blank=True)
	website = models.CharField(max_length=60,blank=True)
	mainimage = ProcessedImageField(upload_to=create_company_image_path, processors=[ResizeToFit(300, 150)],format='JPEG',options={'quality': 60},null=True,blank=True) 
	license_no = models.BigIntegerField(max_length=25)
	email = models.EmailField(max_length=60) # This is the editable contact Email (login email stored in User class)
	phonenumber = models.BigIntegerField(max_length=10,null=True,blank=True)

	# These automatically populate from the zipcode (store for speed purposes)
	zipcode = models.CharField(max_length=20,blank=True)
	city = models.CharField(max_length=100,blank=True)
	county = models.CharField(max_length=100,blank=True)
	state = models.CharField(max_length=100,blank=True)
	phonenumber = models.BigIntegerField(max_length=10,null=True,blank=True)
	
	# Payment and Payout Methods
	balanceduri = models.CharField(max_length=255,blank=True)
	payment_method = models.ForeignKey('payment.Payment',related_name="paymentmethod",null=True,blank=True)
	payout_method = models.ForeignKey('payment.Payment',related_name="payoutmethod",null=True,blank=True)

	# Current credit balance
	credits = models.BigIntegerField(max_length=10,default=0) # Stored for speed purposes

	def __unicode__(self):
		return self.business_name

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
class Supplier(models.Model):
	members = models.ManyToManyField(BasicUser)
	name = models.CharField(max_length=60)
	description = models.TextField()
	website = models.CharField(max_length=60,blank=True,null=True)
	mainimage = ProcessedImageField(upload_to=create_company_image_path, processors=[ResizeToFit(300, 150)],format='JPEG',options={'quality': 60},null=True,blank=True) 

	# Payment and Payout Methods
	balanceduri = models.CharField(max_length=255,blank=True,null=True)
	payout_method = models.ForeignKey('payment.Payment',null=True,blank=True)


############################################
####### Credits ############################
############################################
class Credit(models.Model):
	clinic = models.ForeignKey(Clinic)
	amount = models.IntegerField(max_length=6)
	expires = models.DateTimeField()
	CREDIT_TYPES = (('referral','Friend Referral'),('signup','New Customer'),('promotion','Promotion'))
	credittype = models.CharField(max_length=2,choices=CREDIT_TYPES,default=0)
	referree = models.ForeignKey(BasicUser,related_name="creditreferree",null=True,blank=True)
	purchaseditem = models.ForeignKey('purchase.PurchasedItem',null=True,blank=True)

	def __unicode__(self):
		return self.credittype+ "Credit"

############################################
####### Wishlist Items #####################
############################################
class SavedItem(models.Model):
	user = models.ForeignKey(Clinic)
	item = models.ForeignKey('listing.Product')

############################################
####### Addresses Model  ###################
############################################
class Address(models.Model):
	user = models.ForeignKey(Clinic,null=True,blank=True)
	main_address = models.BooleanField(default=False)
	name = models.CharField(max_length=50) # full name
	address_one = models.CharField(max_length=100) #street address,p.o. box, company name c/o
	address_two = models.CharField(max_length=100,blank=True) #apartment, suite, unit, building,floor,etc.
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100) #Can be state/province/or region
	country = models.CharField(max_length=50, default="United States")
	zipcode = models.CharField(max_length=20) # Can be zipcode or postal code

############################################
### Feedback ###############################
############################################
class Feedback(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(BasicUser)
	love = models.TextField()
	change = models.TextField()

