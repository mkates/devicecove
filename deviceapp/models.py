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
	features = models.TextField()
	manufacturer = models.ForeignKey(Manufacturer)
	mainimage = models.CharField(max_length=100)
	specs = models.CharField(max_length=1000)
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
			
	def __unicode__(self):
		return self.user.username

#An individual item for sale associated with a product and a user
class Item(models.Model):
	product = models.ForeignKey(Product)
	condition = models.IntegerField(max_length=1) #1 being parts only to 6 being new
	type = models.CharField(max_length = 24)
	user = models.ForeignKey(BasicUser)
	description = models.TextField()
	price = models.FloatField(max_length=20)
	picturearray = models.CharField(max_length=100)
	status = models.IntegerField(max_length=1) #1 being inactive, #2 being active, #3 being sold
	savedcount = models.IntegerField()
	def __unicode__(self):
		return self.product.name+" from "+self.user.name
		
	def save(self, *args, **kwargs):
		self.product.totalunits += 1
		self.product.devicecategory.totalunits += 1
		self.product.save()
		self.product.devicecategory.save()
		super(Item, self).save(*args, **kwargs)

class SavedItem(models.Model):
	user = models.ForeignKey(BasicUser)
	item = models.ForeignKey(Item)
	
	
#This function generates a random name for the uploaded image
def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('userimages', filename)
    
class UserImage(models.Model):
	item = models.ForeignKey(Item,blank=True,null=True)
	photo = models.ImageField(upload_to=get_file_path)
