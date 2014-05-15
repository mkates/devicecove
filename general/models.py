from django.db import models

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

############################################
####### Charities  #########################
############################################	
class Charity(models.Model):
	name = models.CharField(max_length=40)
	active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

############################################
#### Feedback Form  ########################
############################################
class Feedback(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey('account.BasicUser')
	love = models.TextField()
	change = models.TextField()

############################################
### Contact Form ###########################
############################################
class Contact(models.Model):
	user = models.ForeignKey('account.BasicUser',null=True,blank=True)
	name = models.CharField(max_length = 50)
	email = models.CharField(max_length = 50)
	message = models.CharField(max_length = 50)

############################################
### Promotional Codes ######################
############################################
class PromoCode(models.Model):
	code = models.CharField(max_length=100,unique=True)
	promo_text = models.CharField(max_length=255) # Fun description
	active = models.BooleanField()
	uses_left = models.IntegerField(max_length=5,default=10000)
	details = models.CharField(max_length=100) # Short description
	discount = models.IntegerField(max_length = 10,null=True,blank=True) # integer discount
	def __unicode__(self):
		return self.code