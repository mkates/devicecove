from django.db import models
from django.contrib.auth.models import User
import uuid, os
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField

############################################
####### Product Database Models ############
############################################

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

class Category(models.Model):
	name = models.CharField(max_length=60)
	displayname = models.CharField(max_length=50)
	industry = models.ForeignKey(Industry)
	totalunits = models.IntegerField(default=0) # Regular script to update this
	def __unicode__(self):
		return self.displayname
	
	## Returns an alphabetical list of it's subcategories ##
	def orderedSubcategories(self):
		return self.subcategory_set.all().order_by('name')

class SubCategory(models.Model):
	name = models.CharField(max_length=60,unique=True)
	displayname = models.CharField(max_length=50)
	category = models.ManyToManyField(Category)
	maincategory = models.ForeignKey(Category,related_name='maincategory')
	totalunits = models.IntegerField(default=0)
	def __unicode__(self):
		return self.displayname
	
############################################
####### Uploaded Images ####################
############################################
#This function generates a random name for the uploaded image
def get_file_path_original(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid.uuid4()), ext)
	return os.path.join('userimages', filename)
def get_file_path_small(instance, filename):
	ext = filename.split('.')[-1]
	filenamesmall = "%s.%s" % (str(uuid.uuid4())+"_small", ext)
	return os.path.join('userimages', filenamesmall)
def get_file_path_medium(instance, filename):
	ext = filename.split('.')[-1]
	filenamemedium = "%s.%s" % (str(uuid.uuid4())+"_medium", ext)
	return os.path.join('userimages', filenamemedium)
		
class Image(models.Model):
	photo = ProcessedImageField(upload_to=get_file_path_original,processors=[ResizeToFit(1300, 1000)],format='JPEG',options={'quality': 60})
	photo_small = ProcessedImageField(upload_to=get_file_path_small, processors=[ResizeToFit(100, 100)],format='JPEG',options={'quality': 60})
	photo_medium = ProcessedImageField(upload_to=get_file_path_medium, processors=[ResizeToFit(500, 500)],format='JPEG',options={'quality': 60})
	id = models.AutoField(primary_key = True)

############################################
####### User Class #########################
############################################	
# Generic User already includes email/password
class BasicUser(models.Model):
	# General
	user = models.OneToOneField(User)
	name = models.CharField(max_length=60)
	email = models.CharField(max_length=60) # Contact Email, login email stored in User class
	age = models.IntegerField(default=0,null=True,blank=True)
	
	# Business Information
	businesstype = models.CharField(max_length=60)
	company = models.CharField(max_length=60)
	website = models.CharField(max_length=60,null=True)
	
	# Default Address
	address_one = models.CharField(max_length=60)
	address_two = models.CharField(max_length=60,null=True,blank=True)
	zipcode = models.IntegerField(max_length=5)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=60)
	phonenumber = models.BigIntegerField(max_length=14)
	
	# User's Rank - Used for specials and promotions
	USER_RANK =  (('0', '0'),('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'))
	user_rank = models.CharField(max_length=20,choices=USER_RANK,default='newb')
	
	# Balanced Payment URI
	balanceduri = models.CharField(max_length=255,null=True,blank=True)
	
	# User's Payment Options
	PAYMENT_OPTIONS =  (('none','None'),('card', 'Credit Card'),('bank', 'Bank Account'))
	payment_method = models.CharField(max_length=20,choices=PAYMENT_OPTIONS,default='none')
	default_payment_cc = models.ForeignKey('BalancedCard',null=True,blank=True) 
	default_payment_ba = models.ForeignKey('BalancedBankAccount',null=True,blank=True,related_name="default_payment_ba") 
	
	# User's Payout Options
	PAYOUT_OPTIONS =  (('none', 'None'),('check', 'Check'),('bank', 'Bank'))
	payout_method = models.CharField(max_length=20,choices=PAYOUT_OPTIONS,default='none')
	default_payout_ba = models.ForeignKey('BalancedBankAccount',null=True,blank=True,related_name="default_payout_ba") 
	check_address = models.ForeignKey('UserAddress',null=True,blank=True)
	
	def __unicode__(self):
		return self.name
	
	#Get number of unanswered questions
	def unansweredQuestionCount(self):
		questions = Question.objects.filter(seller=self)
		count = 0
		for question in questions:
			if not question.answer:
				count += 1
		return count
	
	#Number of asked questions
	def askedQuestionCount(self):
		questions = Question.objects.filter(buyer=self).count()
		return questions
		
	#Number of items in wishlist
	def wishlist(self):
		savedItems = SavedItem.objects.filter(user=self).count()
		return savedItems
	
	#Get counts for each type of listing
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
	
	#Number of Purchases
	def buyhistory(self):
		return PurchasedItem.objects.filter(buyer=self).count()
	
	#Number of Sales
	def sellhistory(self):
		return PurchasedItem.objects.filter(seller=self).count()
		
#An individual item for sale associated with a product and a user
class Item(models.Model):
	### Reference to the user ###
	user = models.ForeignKey(BasicUser)
	listeddate = models.DateField(auto_now_add =True,blank=True)
		
	### General Product Information ###
	name = models.CharField(max_length=200)
	subcategory = models.ForeignKey(SubCategory)
	manufacturer = models.TextField(blank=True)
	
	### Specs ###
	serialno = models.CharField(max_length=30,null=True,blank=True)
	modelyear = models.IntegerField(max_length=4,null=True,blank=True)
	originalowner = models.BooleanField(default=False)
	mainimage = models.ForeignKey(Image,null=True,blank=True)
	
	### Warranty + Service Contracts ###
	CONTRACT_OPTIONS =  (
		('warranty', 'Warranty'),
		('servicecontract', 'Service Contract'),
		('none', 'No Warranty / Service Contract')
	)
	contract = models.CharField(max_length=40, choices=CONTRACT_OPTIONS,default="none")
	contractdescription = models.TextField(blank=True)
	
	### Condition ###
	TYPE_OPTIONS =  (
		('new', 'New'),
		('refurbished', 'Refurbished'),
		('preowned', 'Pre-Owned')
	)
	conditiontype = models.CharField(max_length=20, choices=TYPE_OPTIONS)
	CONDITION_OPTIONS =  (
		(1, 'Parts Only'),
		(2, 'Acceptable'),
		(3, 'Good'),
		(4, 'Like New'),
		(5, 'Brand New')
	)
	conditionquality = models.IntegerField(max_length=10,choices=CONDITION_OPTIONS) #1 being parts only to 5 being brand new
	conditiondescription = models.TextField(blank=True)
	productdescription = models.TextField(blank=True)
	whatsincluded = models.TextField(blank=True)		
	
	### Logistics ###
	shippingincluded = models.BooleanField(default=True)
	offlineviewing = models.BooleanField(default=False)
	tos = models.BooleanField(default=False)
	
	### Pricing ###
	msrp_price = models.BigIntegerField(max_length=20)
	price = models.BigIntegerField(max_length=20)
	
	### Payment ###
	promo_code = models.ForeignKey('PromoCode',blank=True,null=True)
	commission_paid = models.BooleanField(default=False)	
	sold_online = models.BooleanField(default=False) # An offline viewable item was bought online
	
	### Miscellaneous ###
	LISTSTATUS_OPTIONS =  (
		('active', 'Active'),
		('disabled', 'Disabled'),
		('incomplete', 'Incomplete'),
		('sold', 'Sold'),
		('unsold', 'Not Sold')
	)
	liststatus = models.CharField(max_length=30, choices=LISTSTATUS_OPTIONS)
	quantity = models.IntegerField(default=1)
	savedcount = models.IntegerField()
	liststage = models.IntegerField()
	views = models.IntegerField(default=0) # Counts number of page requests
	
	def __unicode__(self):
		return self.name
		
############################################
####### Seller Contact Message #############
############################################
class SellerMessage(models.Model):
	buyer = models.ForeignKey(BasicUser)
	item = models.ForeignKey(Item)
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100,null=True,blank=True)
	phone = models.CharField(max_length=100,null=True,blank=True)
	message = models.TextField(blank=True)
	reason = models.CharField(max_length=100,null=True,blank=True)
	date_sent = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	
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
	zipcode = models.IntegerField(max_length=5, db_index=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	county = models.CharField(max_length=50)
	
############################################
####### Questions Model  ###################
############################################
class Question(models.Model):
	item = models.ForeignKey(Item)
	buyer = models.ForeignKey(BasicUser)
	seller = models.ForeignKey(BasicUser,related_name="seller")
	dateasked = models.DateTimeField(auto_now_add = True,blank=True)
	dateanswered = models.DateTimeField(blank=True,null=True)
	question = models.TextField()
	answer = models.TextField(null=True,blank=True)
	
	def __unicode__(self):
		return self.question

############################################
####### Addresses Model  ###################
############################################
class UserAddress(models.Model):
	user = models.ForeignKey(BasicUser,null=True,blank=True)
	name = models.CharField(max_length=50)
	address_one = models.CharField(max_length=100)
	address_two = models.CharField(max_length=100,null=True,blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zipcode = models.IntegerField(max_length=100)
	phonenumber = models.CharField(max_length=100)

############################################
####### Balanced Models ####################
############################################

#### Balanced Credit Card ##################
class BalancedCard(models.Model):
	user = models.ForeignKey(BasicUser,null=True,blank=True)
	uri = models.CharField(max_length=255)
	brand = models.CharField(max_length=100)
	cardhash = models.CharField(max_length=255)
	expiration_month = models.IntegerField(max_length=2)
	expiration_year = models.IntegerField(max_length=4)
	last_four = models.IntegerField(max_length=4)
	datecreated = models.DateTimeField(auto_now_add = True,blank=True)

#### Balanced Bank Account ##################
class BalancedBankAccount(models.Model):
	user = models.ForeignKey(BasicUser,null=True,blank=True)
	uri = models.CharField(max_length=255)
	fingerprint = models.CharField(max_length=255)
	bank_name = models.CharField(max_length=255)
	bank_code = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	account_number = models.CharField(max_length=255)
	datecreated = models.DateTimeField(auto_now_add = True,blank=True)
	
############################################
####### Checkout Model  ####################
############################################
#### Made up of cart items #################
class Checkout(models.Model):
	
	buyer = models.ForeignKey(BasicUser)
	shipping_address = models.ForeignKey(UserAddress,null=True,blank=True)
	start_time = models.DateTimeField(auto_now_add = True,blank=True)
	
	# User can pay via bank account OR credit card
	PAYMENT_OPTIONS = (('none','none'),('bank','bank'),('card','card'))
	payment_method = models.CharField(default='none',max_length=20, choices=PAYMENT_OPTIONS)
	cc_payment = models.ForeignKey(BalancedCard,null=True,blank=True)
	ba_payment = models.ForeignKey(BalancedBankAccount,null=True,blank=True)
	
	STATE_OPTIONS =  (
		(0, 'login'),
		(1, 'shipping'),
		(2, 'payment'),
		(3, 'review'),
		(4, 'failed_submit'), # If item is sold/other error while submitting checkout
		(5, 'purchased')
	)
	state = models.IntegerField(max_length=1, choices=STATE_OPTIONS)
	
	# Purchase Details, means successfully charged as well
	purchased = models.BooleanField(default=False)
	purchased_time = models.DateTimeField(null=True,blank=True)
	
	#Retrieves the payment object
	def getpayment(self):
		if self.payment_method == 'bank':
			return self.ba_payment
		elif self.payment_method == 'card':
			return self.cc_payment
		else:
			return None
				
	#Get total amount due for this checkout
	def total(self):
		total = 0
		cartitems = self.cartitem_set.all()
		for cartitem in cartitems:
			total += cartitem.price*cartitem.quantity
		return int(total)
	
	#Number of items in cart
	def numberitems(self):
		count = 0
		cartitems = self.cartitem_set.all()
		for cartitem in cartitems:
			count += cartitem.quantity
		return count

############################################
####### Shopping Cart and Cart Items########
############################################	
class ShoppingCart(models.Model):
	user = models.OneToOneField(BasicUser,null=True,blank=True)
	datecreated = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	
	#Get list of items
	def cart_items(self):
		cartitems = CartItem.objects.filter(shoppingcart=self)
		items = []
		for cartitem in cartitems:
			items.append(cartitem.item)
		return items

class CartItem(models.Model):
	checkout = models.ForeignKey(Checkout,null=True,blank=True)
	dateadded = models.DateTimeField(auto_now_add = True,blank=True)
	item = models.ForeignKey(Item)
	price = models.BigIntegerField() # Need price here too in case item's price changes
	shoppingcart = models.ForeignKey(ShoppingCart,null=True,blank=True)
	quantity = models.IntegerField(default=1,max_length=3)
	
	#Finds the number of other shopping carts have this item
	def numbercarts(self):
		return CartItem.objects.filter(item=self.item).count()-1
	
	def amount(self):
		return self.item.price*self.quantity
		
############################################
### Payout Record Keeping ##################
############################################

#### Record of the payment ##################
class BankPayout(models.Model):
	user = models.ForeignKey(BasicUser)
	amount = models.BigIntegerField(max_length=20)
	bank_account = models.ForeignKey(BalancedBankAccount)
	date = models.DateTimeField(auto_now_add = True)

#### Record of all checks ##################
class CheckPayout(models.Model):
	user = models.ForeignKey(BasicUser)
	amount = models.BigIntegerField(max_length=20)
	sent = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add = True)
	address = models.ForeignKey(UserAddress)
	
#### Commission ############################
class Commission(models.Model):
	item = models.OneToOneField(Item)
	amount = models.BigIntegerField(max_length=20)
	PAYMENT_OPTIONS = (('bank','bank'),('card','card'))
	payment_method = models.CharField(default='none',max_length=20, choices=PAYMENT_OPTIONS)
	cc_payment = models.ForeignKey(BalancedCard,null=True,blank=True)
	ba_payment = models.ForeignKey(BalancedBankAccount,null=True,blank=True)
	date = models.DateTimeField(auto_now_add = True)

############################################
### Purchased Items  #######################
############################################	
	
class PurchasedItem(models.Model):
	#Seller and Buyer
	seller = models.ForeignKey(BasicUser,related_name="purchaseditemseller")
	buyer = models.ForeignKey(BasicUser,related_name="purchaseditembuyer")
	
	total = models.BigIntegerField(max_length=20)
	unit_price = models.BigIntegerField(max_length=20)
	# Reference to cart item of the purchase and the checkout
	cartitem = models.OneToOneField(CartItem)
	checkout = models.ForeignKey(Checkout)
	
	quantity = models.IntegerField(max_length = 5)
	item_name = models.CharField(max_length=300)
	
	purchase_date = models.DateTimeField(auto_now_add = True)
	
	# Post Purchase
	item_sent = models.BooleanField(default=False)
	seller_message = models.TextField(blank=True)
	buyer_message = models.TextField(blank=True)
	# Seller Payment
	paid_out = models.BooleanField(default=False)
	paid_date = models.DateTimeField(null=True,blank=True)
	
	#should replicate payout in the checkout
	PAYOUT_OPTIONS =  (('none', 'None'),('check', 'Check'),('bank', 'Bank'))
	payout_method = models.CharField(max_length=20,choices=PAYOUT_OPTIONS,default='none')
	
	#References to the actual payout objects
	online_payment = models.ForeignKey(BankPayout,null=True,blank=True)
	check = models.ForeignKey(CheckPayout,null=True,blank=True)
	
############################################
### Item Reviews ###########################
############################################	
class SellerReview(models.Model):
	seller = models.ForeignKey(BasicUser,related_name="sellerreviewseller")
	buyer = models.ForeignKey(BasicUser,related_name="sellerreviewbuyer")
	REVIEW_OPTIONS =  (('negative', 'Negative'),('neutral', 'Neutral'),('positive', 'Positive'))
	review_rating = models.IntegerField(max_length = 20,choices=REVIEW_OPTIONS)
	review = models.TextField(blank=True)

class ItemReview(models.Model):
	seller = models.ForeignKey(BasicUser,related_name="itemreview_seller")
	buyer = models.ForeignKey(BasicUser,related_name="itemreview_buyer")
	item = models.ForeignKey(PurchasedItem)
	REVIEW_OPTIONS =  (('negative', 'Negative'),('neutral', 'Neutral'),('positive', 'Positive'))
	review_rating = models.IntegerField(max_length = 20,choices=REVIEW_OPTIONS)
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
### Reminder Email Responses ###############
############################################
class ReminderToken(models.Model):
	contact_message = models.ForeignKey(SellerMessage)
	ACTION_OPTIONS =  (('none', 'None'),('sold', 'Sold'),('not_sold', 'Not Sold'),('different_sold','Different Buyer'))
	action = models.CharField(max_length = 50,choices=ACTION_OPTIONS,default="none")
	token = models.CharField(max_length = 20,unique=True)

############################################
### Promotional Codes ######################
############################################
class PromoCode(models.Model):
	code = models.CharField(max_length=100,unique=True)
	promo_text = models.CharField(max_length=255) # Fun description
	active = models.BooleanField()
	details = models.CharField(max_length=100) # Short description
	PROMO_TYPE =  (('factor', 'Factor'),('discount', 'Discount'))
	promo_type = models.CharField(max_length = 50,choices=PROMO_TYPE)
	factor = models.IntegerField(max_length=100,null=True,blank=True) # % off commission / 100
	discount = models.IntegerField(max_length = 10,null=True,blank=True) # straight discount

