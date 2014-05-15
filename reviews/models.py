from django.db import models

##############################################
####### Reviews App ##########################
##############################################

# Create your models here.
class Review(models.Model):
	creation_date = models.DateTimeField(auto_now_add=True)
	last_edit = models.DateTimeField(auto_now_add=True)
	product = models.ForeignKey('listing.Product')
	clinic = models.ForeignKey('account.Clinic')
	rating = models.IntegerField(max_length=1,default=3)
	review = models.TextField()
	reviewer = models.CharField(max_length=100)
	item = models.ForeignKey('listing.Item',null=True,blank=True) # Is it a verified review? What item did they buy
	item_quantity = models.IntegerField(max_length=6,default=0) # The number of times they purchased the item
	upvotes = models.IntegerField(max_length=6,default=0) #Updated via script

class Upvote(models.Model):
	creation_date = models.DateTimeField(auto_now_add=True)
	clinic = models.ForeignKey('account.Clinic')
	review = models.ForeignKey(Review)

