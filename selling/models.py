from django.db import models

############################################
####### Seller Contact Message #############
############################################
class SellerMessage(models.Model):
	buyer = models.ForeignKey('account.BasicUser')
	item = models.ForeignKey('listing.Item')
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100,blank=True)
	phone = models.CharField(max_length=100,blank=True)
	message = models.TextField(blank=True)
	reason = models.CharField(max_length=100,blank=True)
	date_sent = models.DateTimeField(auto_now_add=True)
	
	#Checks if the message's buyer can purchase this item online
	def authorizedBuyer(self):
		return True if BuyAuthorization.objects.filter(buyer=self.buyer,seller=self.item.user,item=self.item).exists() else False	

############################################
### Item Reviews ###########################
############################################	
class SellerReview(models.Model):
	seller = models.ForeignKey('account.BasicUser',related_name="sellerreview_seller")
	buyer = models.ForeignKey('account.BasicUser',related_name="sellerreview_buyer")
	date = models.DateTimeField(auto_now_add = True)
	REVIEW_OPTIONS =  (('negative', 'Negative'),('neutral', 'Neutral'),('positive', 'Positive'))
	review_rating = models.CharField(max_length = 20,choices=REVIEW_OPTIONS)
	review = models.TextField(blank=True)

class ItemReview(models.Model):
	seller = models.ForeignKey('account.BasicUser',related_name="itemreview_seller")
	buyer = models.ForeignKey('account.BasicUser',related_name="itemreview_buyer")
	date = models.DateTimeField(auto_now_add = True)
	item = models.ForeignKey('purchase.PurchasedItem')
	REVIEW_OPTIONS =  (('negative', 'Negative'),('neutral', 'Neutral'),('positive', 'Positive'))
	review_rating = models.CharField(max_length = 20,choices=REVIEW_OPTIONS)
	review = models.TextField(blank=True)

############################################
### Report #################################
############################################	
class Report(models.Model):
	purchased_item = models.OneToOneField('purchase.PurchasedItem')
	reason = models.CharField(max_length=100)
	details = models.TextField()
	
############################################
### Inactive Request #######################
############################################
class InactiveRequest(models.Model):
	item = models.ForeignKey('listing.Item')
	reason = models.TextField()
	date_submitted = models.DateTimeField(auto_now_add = True)
	
############################################
### Offline Authorizations #################
############################################
class BuyAuthorization(models.Model):
	seller = models.ForeignKey('account.BasicUser',related_name="authorizedseller")
	buyer = models.ForeignKey('account.BasicUser',related_name="authorizedbuyer")
	item = models.ForeignKey('listing.Item')
	date = models.DateTimeField(auto_now_add = True)

############################################
### Contact Message Reminder Email #########
############################################
class ReminderToken(models.Model):
	contact_message = models.ForeignKey(SellerMessage)
	ACTION_OPTIONS =  (('none', 'None'),('sold', 'Sold'),('not_sold', 'Not Sold'),('different_sold','Different Buyer'))
	action = models.CharField(max_length = 50,choices=ACTION_OPTIONS,default='none')
	token = models.CharField(max_length = 20,unique=True)

