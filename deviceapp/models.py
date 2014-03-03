from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

############################################
####### User Class #########################
############################################	
# Generic User already includes email/password
class BasicUser(models.Model):
	# General
	creation_date = models.DateField(auto_now_add=True)
	user = models.OneToOneField(User)
	firstname = models.CharField(max_length=60)
	lastname = models.CharField(max_length=60)
	email = models.EmailField(max_length=60) # Contact Email, login email stored in User class
	zipcode = models.IntegerField(max_length=5)
	
	# These automatically populate from the zipcode (store for speed purposes)
	city = models.CharField(max_length=100,blank=True)
	county = models.CharField(max_length=100,blank=True)
	state = models.CharField(max_length=100,blank=True)
	
	# Additional Business Information (if they are a seller)
	businesstype = models.CharField(max_length=60,blank=True)
	company = models.CharField(max_length=60,blank=True)
	website = models.CharField(max_length=60,blank=True)
	phonenumber = models.BigIntegerField(max_length=10,null=True,blank=True)
	
	# User's Rank (will be used for different commission classes, listing limits, etc.)
	USER_RANK =  ((0, 0),(1, 1),(2, 2),(3, 3),(4, 4),(5, 5))
	user_rank = models.IntegerField(max_length=2,choices=USER_RANK,default=0)
	
	# Payments
	balanceduri = models.CharField(max_length=255,blank=True)
	payment_method = models.ForeignKey('Payment',related_name="paymentmethod",null=True,blank=True)
	payout_method = models.ForeignKey('Payment',related_name="payoutmethod",null=True,blank=True)
	
	# Settings 
	newsletter = models.BooleanField(default=True)

	def name(self):
		return self.firstname+" "+self.lastname

	def __unicode__(self):
		return self.firstname+" "+self.lastname
		
	# Get number of unanswered questions
	def unansweredQuestionCount(self):
		return Question.objects.filter(seller=self).filter(answer = "").count()
		
	# Number of asked questions
	def askedQuestionCount(self):
		return Question.objects.filter(buyer=self).count()
		
	# Number of items in wishlist
	def wishlist(self):
		return SavedItem.objects.filter(user=self).count()
	
	#Get counts for each type of listing (used in profile page)
	# 'all' and 'inactive' are cumulative counts
	def listedItemCount(self):
		dict = {'all':0,'inactive':0,'sold':0,'unsold':0,'active':0,'incomplete':0,'disabled':0}
		for item in Item.objects.filter(user=self):
			dict[item.liststatus] += 1
			if item.liststatus != 'disabled':
				dict['all'] += 1
			if item.liststatus == 'sold' or item.liststatus == 'unsold':
				dict['inactive'] += 1
		return dict
	
	# Number of Purchases
	def buyhistory(self):
		return PurchasedItem.objects.filter(buyer=self).count()
	
	# Number of Sales
	def sellhistory(self):
		return PurchasedItem.objects.filter(seller=self).count()

############################################
####### Seller Contact Message #############
############################################
class SellerMessage(models.Model):
	buyer = models.ForeignKey(BasicUser)
	item = models.ForeignKey(Item)
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
####### Wishlist Items #####################
############################################
class SavedItem(models.Model):
	user = models.ForeignKey(BasicUser)
	item = models.ForeignKey(Item)

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
####### Addresses Model  ###################
############################################
class Address(models.Model):
	user = models.ForeignKey(BasicUser,null=True,blank=True)
	name = models.CharField(max_length=50)
	address_one = models.CharField(max_length=100)
	address_two = models.CharField(max_length=100,blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zipcode = models.IntegerField(max_length=100)
	phonenumber = models.CharField(max_length=100)

############################################
####### Payment Models #####################
############################################

class Payment(models.Model):
	user = models.ForeignKey(BasicUser,null=True,blank=True)
	datecreated = models.DateTimeField(auto_now_add=True)
	
#### Payment/Payout by Check ##################
class CheckAddress(Payment):
	address = models.ForeignKey(Address)

#### Balanced Credit Card ##################
class BalancedCard(Payment):
	uri = models.CharField(max_length=255)
	brand = models.CharField(max_length=100)
	cardhash = models.CharField(max_length=255)
	expiration_month = models.IntegerField(max_length=2)
	expiration_year = models.IntegerField(max_length=4)
	last_four = models.IntegerField(max_length=4)

#### Balanced Bank Account ##################
class BalancedBankAccount(Payment):
	uri = models.CharField(max_length=255)
	fingerprint = models.CharField(max_length=255)
	bank_name = models.CharField(max_length=255)
	bank_code = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	account_number = models.CharField(max_length=255)

############################################
### Payout Record Keeping ##################
############################################

class Payout(models.Model):
	user = models.ForeignKey(BasicUser)
	amount = models.BigIntegerField(max_length=20)
	date = models.DateTimeField(auto_now_add = True)
	total_commission = models.BigIntegerField(max_length=20)
	total_charity = models.BigIntegerField(max_length=20)
	cc_fee = models.BigIntegerField(max_length=20)
	
	def subtotal(self):
		return self.amount+self.total_commission+self.cc_fee+self.total_charity
	
#### Record of the bank payout ##################
class BankPayout(Payout):
	bank_account = models.ForeignKey(BalancedBankAccount)
	STATUS_OPTIONS =  (('failed', 'Failed'),('pending', 'Pending'),('paid', 'Paid'))
	status = models.CharField(max_length=20,choices=STATUS_OPTIONS,default='pending')
	transaction_number = models.CharField(max_length=30)
	events_uri = models.CharField(max_length=200)
		
#### Record of the check payout ##################
class CheckPayout(Payout):
	address = models.ForeignKey(CheckAddress)
	sent = models.BooleanField(default=False)

############################################
####### Commission #########################
############################################

class Commission(models.Model):
	item = models.OneToOneField(Item)
	price = models.BigIntegerField(max_length=12) #Price of the item
	amount = models.BigIntegerField(max_length=20) #Commission amount
	payment = models.ForeignKey(Payment) # Can only be a card or bank account
	date = models.DateTimeField(auto_now_add = True)
	transaction_number = models.CharField(max_length=40)
		

############################################
### Purchased Items  #######################
############################################	

class Order(models.Model):
	buyer = models.ForeignKey(BasicUser)
	payment = models.ForeignKey(Payment,null=True,blank=True)
	purchase_date = models.DateTimeField(auto_now_add = True)
	total = models.BigIntegerField(max_length=20)
	tax = models.BigIntegerField(max_length=13,default=0)
	shipping_address = models.ForeignKey(Address,null=True,blank=True) # Can be null if pick-up only item
	transaction_number = models.CharField(max_length=40)

class PurchasedItem(models.Model):
	purchase_date = models.DateTimeField(auto_now_add = True)

	# Seller and Buyer
	seller = models.ForeignKey(BasicUser,related_name="purchaseditemseller")
	buyer = models.ForeignKey(BasicUser,related_name="purchaseditembuyer")
	order = models.ForeignKey(Order)
	
	# Details
	item = models.ForeignKey(Item)
	quantity = models.IntegerField(max_length = 5)
	unit_price = models.BigIntegerField(max_length=20)
	item_name = models.CharField(max_length=300)
	
	# Deductions
	charity = models.BooleanField(default=False)
	charity_name = models.ForeignKey(Charity,null=True,blank=True)
	promo_code = models.ForeignKey(PromoCode,null=True,blank=True)
	commission = models.BigIntegerField(max_length=14)

	# Post Purchase
	shipping_included = models.BooleanField(default=True)
	item_sent = models.BooleanField(default=False)
	seller_message = models.TextField(blank=True)
	buyer_message = models.TextField(blank=True)
	
	# Seller Payment
	paid_out = models.BooleanField(default=False)
	paid_date = models.DateTimeField(null=True,blank=True)
	payout = models.ForeignKey(Payout,null=True,blank=True)
	
	def total(self):
		return self.unit_price*self.quantity

############################################
### Item Reviews ###########################
############################################	
class SellerReview(models.Model):
	seller = models.ForeignKey(BasicUser,related_name="sellerreview_seller")
	buyer = models.ForeignKey(BasicUser,related_name="sellerreview_buyer")
	date = models.DateTimeField(auto_now_add = True)
	REVIEW_OPTIONS =  (('negative', 'Negative'),('neutral', 'Neutral'),('positive', 'Positive'))
	review_rating = models.CharField(max_length = 20,choices=REVIEW_OPTIONS)
	review = models.TextField(blank=True)

class ItemReview(models.Model):
	seller = models.ForeignKey(BasicUser,related_name="itemreview_seller")
	buyer = models.ForeignKey(BasicUser,related_name="itemreview_buyer")
	date = models.DateTimeField(auto_now_add = True)
	item = models.ForeignKey(PurchasedItem)
	REVIEW_OPTIONS =  (('negative', 'Negative'),('neutral', 'Neutral'),('positive', 'Positive'))
	review_rating = models.CharField(max_length = 20,choices=REVIEW_OPTIONS)
	review = models.TextField(blank=True)

############################################
### Report #################################
############################################	
class Report(models.Model):
	purchased_item = models.OneToOneField(PurchasedItem)
	reason = models.CharField(max_length=100)
	details = models.TextField()
	
############################################
### Inactive Request #######################
############################################
class InactiveRequest(models.Model):
	item = models.ForeignKey(Item)
	reason = models.TextField()
	date_submitted = models.DateTimeField(auto_now_add = True)
	
############################################
### Offline Authorizations #################
############################################
class BuyAuthorization(models.Model):
	seller = models.ForeignKey(BasicUser,related_name="authorizedseller")
	buyer = models.ForeignKey(BasicUser,related_name="authorizedbuyer")
	item = models.ForeignKey(Item)
	date = models.DateTimeField(auto_now_add = True)

############################################
### Contact Message Reminder Email #########
############################################
class ReminderToken(models.Model):
	contact_message = models.ForeignKey(SellerMessage)
	ACTION_OPTIONS =  (('none', 'None'),('sold', 'Sold'),('not_sold', 'Not Sold'),('different_sold','Different Buyer'))
	action = models.CharField(max_length = 50,choices=ACTION_OPTIONS,default='none')
	token = models.CharField(max_length = 20,unique=True)

############################################
### Price Changes  #########################
############################################
# Store all price changes of items #########
class PriceChange(models.Model):
	item = models.ForeignKey(Item)
	date_changed = models.DateTimeField(auto_now_add = True)
	original_price = models.BigIntegerField(max_length = 14)
	new_price = models.BigIntegerField(max_length = 14)

############################################
### Contact Form ###########################
############################################
class Contact(models.Model):
	user = models.ForeignKey(BasicUser,null=True,blank=True)
	name = models.CharField(max_length = 50)
	email = models.CharField(max_length = 50)
	message = models.CharField(max_length = 50)












