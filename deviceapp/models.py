from django.db import models
from django.contrib.auth.models import User

############################################
####### Product Database Models ############
############################################

# Industry
class Industry(models.Model):
	name = models.CharField(max_length=40)
	def __unicode__(self):
		return self.name

# Device Category (ex. ultrasounds)
class DeviceCategory(models.Model):
	name = models.CharField(max_length=60)
	industries = models.ManyToManyField(Industry)
	def __unicode__(self):
		return self.name

# SubDevice Category (ex. portable ultrasounds)
# Belongs to a device category
class DeviceSubCategory(models.Model):
	name = models.CharField(max_length=60)
	devicecategory = models.ForeignKey(DeviceCategory)
	def __unicode__(self):
		return self.name

# A product, which belongs to a device subcategory
class Product(models.Model):
	name = models.CharField(max_length=60)
	devicesubcategory = models.ForeignKey(DeviceSubCategory)
	industries = models.ManyToManyField(Industry)
	def __unicode__(self):
		return self.name

############################################
####### Users Database #####################
############################################

# Generic User email/password already includes

class BasicUser(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=60)
	zipcode = models.IntegerField(max_length=5)
	businesstype = models.CharField(max_length=60)
	company = models.CharField(max_length=60)
	name = models.CharField(max_length=60)
	email = models.CharField(max_length=60)
	address = models.CharField(max_length=60)
	zipcode = models.CharField(max_length=60)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=60)
	website = models.CharField(max_length=60)
	phonenumber = models.IntegerField(max_length=60)
	password = models.CharField(max_length=60)
			
	def __unicode__(self):
		return self.user.username
	