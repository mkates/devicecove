from django.db import models

############################################
### Contact Form ###########################
############################################
class Contact(models.Model):
	user = models.ForeignKey('account.BasicUser',null=True,blank=True)
	name = models.CharField(max_length = 50)
	email = models.CharField(max_length = 50)
	message = models.CharField(max_length = 50)

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