from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from sorl.thumbnail import ImageField
############################################
####### Product Database Models ############
############################################

# Industry
class Industry(models.Model):
	name = models.CharField(max_length=40)
	def __unicode__(self):
		return self.name

class Manufacturer(models.Model):
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name
	
# Device Category (ex. ultrasounds)
class DeviceCategory(models.Model):
	name = models.CharField(max_length=60)
	industries = models.ManyToManyField(Industry)
	totalunits = models.IntegerField()
	def __unicode__(self):
		return self.name

# A product (i.e. Ultrasound XT500), which belongs to a device subcategory
class Product(models.Model):
	name = models.CharField(max_length=150)
	devicecategory = models.ForeignKey(DeviceCategory)
	industries = models.ManyToManyField(Industry)
	description = models.TextField()
	features = models.TextField()
	manufacturer = models.ForeignKey(Manufacturer)
	mainimage = models.CharField(max_length=100)
	totalunits = models.IntegerField()
	def __unicode__(self):
		return self.name
	
############################################
####### Users Database #####################
############################################

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
	password = models.CharField(max_length=60)
			
	def __unicode__(self):
		return self.user.username
		
#A one-to-many which stores the list of items a basic user has saved		
class SavedItem(models.Model):
	user = models.ForeignKey(BasicUser)
	product = models.ForeignKey(Product)
		
#An individual item for sale associated with a product and a user
class Item(models.Model):
	product = models.ForeignKey(Product)
	condition = models.IntegerField(max_length=1) #1 being parts only to 6 being new
	user = models.ForeignKey(BasicUser)
	description = models.TextField()
	price = models.FloatField(max_length=20)
	def __unicode__(self):
		return self.product.name+" from "+self.user.name
	def save(self, *args, **kwargs):
		self.product.totalunits += 1
		self.product.devicecategory.totalunits += 1
		self.product.save()
		self.product.devicecategory.save()
		super(Item, self).save(*args, **kwargs)
	
class UserImage(models.Model):
	item = models.ForeignKey(Item)
	#userimageurl = models.CharField(max_length=200)	

#This function generates a random name for the uploaded image
def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('userimages', filename)
    
class TestImage(models.Model):
	name = models.CharField(max_length=100)
	photo = models.ImageField(upload_to=get_file_path)
	thumbnail =  models.ImageField(upload_to=get_file_path)