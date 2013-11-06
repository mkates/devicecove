from django.db import models
from django.contrib.auth.models import User
import uuid
import os
############################################
####### Product Database Models ############
############################################

# Industry
class Industry(models.Model):
	name = models.CharField(max_length=40)
	displayname = models.CharField(max_length=50)
	def __unicode__(self):
		return self.displayname

class Manufacturer(models.Model):
	name = models.CharField(max_length=100)
	displayname = models.CharField(max_length=50)
	def __unicode__(self):
		return self.displayname
	
# Device Category (ex. ultrasounds)
class DeviceCategory(models.Model):
	name = models.CharField(max_length=60)
	displayname = models.CharField(max_length=50)
	industries = models.ManyToManyField(Industry)
	totalunits = models.IntegerField()
	def __unicode__(self):
		return self.displayname

# A product (i.e. Ultrasound XT500), which belongs to a device subcategory
class Product(models.Model):
	name = models.CharField(max_length=150)
	devicecategory = models.ForeignKey(DeviceCategory)
	industries = models.ManyToManyField(Industry)
	description = models.TextField()
	manufacturer = models.ForeignKey(Manufacturer)
	specs = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.name
	
############################################
####### Users Database #####################
############################################
#This function generates a random name for the uploaded image
def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('userimages', filename)

class Image(models.Model):
	photo = models.ImageField(upload_to=get_file_path)
	id = models.AutoField(primary_key = True)
	
# Generic User already includes email/password

class BasicUser(models.Model):
	user = models.OneToOneField(User)
	businesstype = models.CharField(max_length=60)
	name = models.CharField(max_length=60)
	company = models.CharField(max_length=60)
	email = models.CharField(max_length=60)
	address = models.CharField(max_length=60)
	zipcode = models.IntegerField(max_length=5)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=60)
	website = models.CharField(max_length=60,null=True)
	phonenumber = models.CharField(max_length=60)
			
	def __unicode__(self):
		return self.user.username

#An individual item for sale associated with a product and a user
class Item(models.Model):
	user = models.ForeignKey(BasicUser)
	
	#General Product Information
	name = models.CharField(max_length=200)
	product = models.ForeignKey(Product,null=True,blank=True)
	devicecategory = models.ForeignKey(DeviceCategory)
	manufacturer = models.ForeignKey(Manufacturer)
	
	#Specs
	serialno = models.CharField(max_length=30,blank=True)
	year = models.IntegerField(max_length=4)
	TYPE_OPTIONS =  (
		('new', 'New'),
		('refurbished', 'Refurbished'),
		('preowned', 'Pre-Owned')
	)
	type = models.CharField(max_length=20, choices=TYPE_OPTIONS)
	dateacquired = models.DateField()
	CONTRACT_OPTIONS =  (
		('contractincluded', 'Service Contract Included'),
		('contractoptional', 'Service Contact Optional'),
		('contractnone', 'No Service Contract')
	)
	contract = models.CharField(max_length=30, choices=CONTRACT_OPTIONS)
	
	#Product Specifics
	condition = models.IntegerField(max_length=1) #1 being parts only to 6 being brand new
	conditiondescription = models.TextField()
	productdescription = models.TextField()
	shippingincluded = models.BooleanField()
	price = models.FloatField(max_length=20)
	mainimage = models.ForeignKey(Image,null=True)
	
	#Miscellaneous 
	LISTSTATUS_OPTIONS =  (
		('active', 'Active'),
		('inactive', 'Inactive'),
		('sold', 'Sold'),
		('deleted', 'Deleted')
	)
	liststatus = models.CharField(max_length=30, choices=LISTSTATUS_OPTIONS)
	savedcount = models.IntegerField()
	verified = models.BooleanField()
	listeddate = models.DateField(auto_now_add = True,blank=True)

	def __unicode__(self):
		return self.name+" from "+self.user.name
		
	def save(self, *args, **kwargs):
		self.devicecategory.totalunits += 1
		self.devicecategory.save()
		super(Item, self).save(*args, **kwargs)

class SavedItem(models.Model):
	user = models.ForeignKey(BasicUser)
	item = models.ForeignKey(Item)

	
class ProductImage(Image):
	item = models.ManyToManyField(Item)
	product = models.ForeignKey(Product)

#Should be a one to one field
class ItemImage(Image):
	item = models.ForeignKey(Item,blank=True,null=True)	

