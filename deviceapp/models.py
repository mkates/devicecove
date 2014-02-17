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
	totalunits = models.IntegerField(default=0) # Script updates this
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
	totalunits = models.IntegerField(default=0) # Script updates this
	
	def __unicode__(self):
		return self.displayname


############################################
####### Charities  #########################
############################################	
class Charity(models.Model):
	name = models.CharField(max_length=40)
	active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

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

############################################
####### User Class #########################
############################################	
# Generic User already includes email/password
class BasicUser(models.Model):
	# General
	user = models.OneToOneField(User)
	name = models.CharField(max_length=60)
	email = models.EmailField(max_length=60) # Contact Email, login email stored in User class
	zipcode = models.IntegerField(max_length=5)
	
	# These automatically populate from the zipcode (stored for speed purposes)
	city = models.CharField(max_length=100,blank=True)
	county = models.CharField(max_length=100,blank=True)
	state = models.CharField(max_length=100,blank=True)
	
	# Additional Business Information (if they are a seller)
	businesstype = models.CharField(max_length=60,blank=True)
	company = models.CharField(max_length=60,blank=True)
	website = models.CharField(max_length=60,blank=True)
	phonenumber = models.BigIntegerField(max_length=10,null=True,blank=True)
	
	# User's Rank - Used for specials, promotions, commission tiers, etc. 
	USER_RANK =  ((0, 0),(1, 1),(2, 2),(3, 3),(4, 4),(5, 5))
	user_rank = models.IntegerField(max_length=2,choices=USER_RANK,default=0)
	
	# Payments
	balanceduri = models.CharField(max_length=255,blank=True)
	payment_method = models.ForeignKey('Payment',related_name="paymentmethod",null=True,blank=True)
	payout_method = models.ForeignKey('Payment',related_name="payoutmethod",null=True,blank=True)
	
	# Settings 
	newsletter = models.BooleanField(default=True)

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
		
# An individual item for sale associated with a product and a user
class Item(models.Model):
	### Reference to the user ###
	user = models.ForeignKey(BasicUser)
	creation_date = models.DateField(auto_now_add=True)
		
	### General Product Information ###
	name = models.CharField(max_length=200)
	subcategory = models.ForeignKey(SubCategory)
	manufacturer = models.TextField(blank=True)
	
	### Specs ###
	serialno = models.CharField(max_length=30,null=True,blank=True)
	modelyear = models.IntegerField(max_length=4,null=True,blank=True)
	originalowner = models.BooleanField(default=False)
	mainimage = models.ForeignKey('Image',related_name="mainitemimage",null=True,blank=True)
	
	### Warranty + Service Contracts ###
	CONTRACT_OPTIONS =  (
		('warranty', 'Warranty'),
		('servicecontract', 'Service Contract'),
		('none', 'None')
	)
	contract = models.CharField(max_length=40, choices=CONTRACT_OPTIONS,default="none")
	contractdescription = models.TextField(blank=True)
	
	### Condition ###
	TYPE_OPTIONS =  (
		('new', 'New'),
		('refurbished', 'Refurbished'),
		('preowned', 'Pre-Owned')
	)
	conditiontype = models.CharField(max_length=20, choices=TYPE_OPTIONS,default="preowned")
	CONDITION_OPTIONS =  (
		(1, 'Parts Only / Not Working'),
		(2, 'Functional with Defects'),
		(3, 'Used Fully Functional'),
		(4, 'Used Like New'),
		(5, 'Brand New')
	)
	conditionquality = models.IntegerField(max_length=10,choices=CONDITION_OPTIONS,default=3)
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
	quantity = models.IntegerField(default=1)
	
	### Payment ###
	promo_code = models.ForeignKey(PromoCode,blank=True,null=True)
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

	### Charity ###
	charity = models.BooleanField(default=False)
	charity_name = models.ForeignKey(Charity,null=True,blank=True)

	liststatus = models.CharField(max_length=30,choices=LISTSTATUS_OPTIONS,db_index=True,default='incomplete')
	liststage = models.IntegerField(default=0)
	savedcount = models.IntegerField(default=0)
	views = models.IntegerField(default=0) # Counts number of page requests
	
	def __unicode__(self):
		return self.name
	
	def msrp_discount(self):
		return int((self.price-self.msrp_price)/float(self.price)*100)


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
	item = models.ForeignKey(Item)
	photo = ProcessedImageField(upload_to=get_file_path_original,processors=[ResizeToFit(1300, 1000)],format='JPEG',options={'quality': 60})
	photo_small = ProcessedImageField(upload_to=get_file_path_small, processors=[ResizeToFit(100, 100)],format='JPEG',options={'quality': 60})
	photo_medium = ProcessedImageField(upload_to=get_file_path_medium, processors=[ResizeToFit(500, 500)],format='JPEG',options={'quality': 60})

############################################
####### Notification Center ################
############################################

class Notification(models.Model):
	user = models.ForeignKey(BasicUser)
	date = models.DateTimeField(auto_now_add=True)
	viewed = models.BooleanField(default=False)

# When buyer messages the seller about an offline item
class SellerMessageNotification(Notification):
	sellermessage = models.ForeignKey('SellerMessage')

# When a seller has a new question
class SellerQuestionNotification(Notification):
	question = models.ForeignKey('Question')

# When a buyer asks a question that is answered
class BuyerQuestionNotification(Notification):
	question = models.ForeignKey('Question')

# When a seller authorizes a buyer to purchase online
class AuthorizedBuyerNotification(Notification):
	item = models.ForeignKey('Item')

# When an item is sold - seller
class SoldNotification(Notification):
	purchaseditem = models.ForeignKey('PurchasedItem')

# Check payment clears if it is a check
class SoldPaymentNotification(Notification):
	purchaseditem = models.ForeignKey('PurchasedItem')

class ShippedNotification(Notification):
	purchaseditem = models.ForeignKey('PurchasedItem')

# When a seller is paid out 
class PayoutNotification(Notification):
	payout = models.ForeignKey('Payout',null=True,blank=True)
	success = models.BooleanField(default=True)

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
####### Questions Model  ###################
############################################
class Question(models.Model):
	item = models.ForeignKey(Item)
	buyer = models.ForeignKey(BasicUser)
	seller = models.ForeignKey(BasicUser,related_name="seller")
	dateasked = models.DateTimeField(auto_now_add = True)
	dateanswered = models.DateTimeField(blank=True,null=True)
	question = models.TextField()
	answer = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.question

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
	
#### Mailing Payout ##################
class CheckAddress(Payment):
	address = models.ForeignKey(Address)

### Mailing Payment ##################
class CheckPayment(Payment):
	received = models.BooleanField(default=False)

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
####### Checkout Model  ####################
############################################
#### Made up of cart items #################
class Checkout(models.Model):	
	buyer = models.ForeignKey(BasicUser)
	shipping_address = models.ForeignKey(Address,null=True,blank=True)
	start_time = models.DateTimeField(auto_now_add = True,blank=True)
	payment = models.ForeignKey(Payment,null=True,blank=True)
	
	STATE_OPTIONS =  ((0, 'login'),(1, 'shipping'),(2, 'payment'),(3, 'review'),(4, 'failed_submit'),(5, 'purchased'))
	state = models.IntegerField(max_length=1, choices=STATE_OPTIONS)
	
	# Purchase Details, means successfully charged as well
	purchased = models.BooleanField(default=False)
	purchased_time = models.DateTimeField(null=True,blank=True)
	
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

	# Is shipping address required?
	def shippingAddressRequired(self):
		for cartitem in self.cartitem_set.all():
			if cartitem.item.shippingincluded:
				return True
		return False

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
	dateadded = models.DateTimeField(auto_now_add = True)
	item = models.ForeignKey(Item)
	price = models.BigIntegerField() # In case price changes during checkout
	shoppingcart = models.ForeignKey(ShoppingCart,null=True,blank=True)
	quantity = models.IntegerField(default=1,max_length=4)
	
	# Finds the number of other shopping carts that have this item
	def numbercarts(self):
		return CartItem.objects.filter(item=self.item).count()-1
	
	def amount(self):
		return self.item.price*self.quantity
		
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
		return self.amount+self.total_commission+self.cc_fee
	
#### Record of the payment ##################
class BankPayout(Payout):
	bank_account = models.ForeignKey(BalancedBankAccount)
	def subtotal(self):
		return self.amount+self.total_commission+self.cc_fee
		
#### Record of all checks ##################
class CheckPayout(Payout):
	address = models.ForeignKey(Address)
	sent = models.BooleanField(default=False)

############################################
### Offline Commission #####################
############################################

#### Commission ############################
class Commission(models.Model):
	item = models.OneToOneField(Item)
	price = models.BigIntegerField(max_length=12)
	amount = models.BigIntegerField(max_length=20)
	payment = models.ForeignKey(Payment) # Can only be a card or bank account
	date = models.DateTimeField(auto_now_add = True)
	transcation_number = models.CharField(max_length=40)

############################################
### Purchased Items  #######################
############################################	

class Order(models.Model):
	buyer = models.ForeignKey(BasicUser)
	payment = models.ForeignKey(Payment,null=True,blank=True)
	purchase_date = models.DateTimeField(auto_now_add = True)
	total = models.BigIntegerField(max_length=20)

class PurchasedItem(models.Model):
	# Seller and Buyer
	seller = models.ForeignKey(BasicUser,related_name="purchaseditemseller")
	buyer = models.ForeignKey(BasicUser,related_name="purchaseditembuyer")
	order = models.ForeignKey(Order)
	
	# Details
	quantity = models.IntegerField(max_length = 5)
	total = models.BigIntegerField(max_length=20)
	unit_price = models.BigIntegerField(max_length=20)
	item_name = models.CharField(max_length=300)
	purchase_date = models.DateTimeField(auto_now_add = True)
	shipping_address = models.ForeignKey(Address,null=True,blank=True) # Can be null if pick-up only item
	
	# Reference to cart item of the purchase and the checkout
	cartitem = models.OneToOneField(CartItem)
	checkout = models.ForeignKey(Checkout)
	
	# Deductions
	charity = models.BooleanField(default=False)
	charity_name = models.ForeignKey(Charity,null=True,blank=True)
	commission = models.BigIntegerField(max_length=14)

	# Post Purchase
	shipping_included = models.BooleanField(default=True)
	item_sent = models.BooleanField(default=False)
	seller_message = models.TextField(blank=True)
	buyer_message = models.TextField(blank=True)
	
	# Seller Payment
	paid_out = models.BooleanField(default=False)
	paid_date = models.DateTimeField(null=True,blank=True)
	
	# Paying Out
	payout = models.ForeignKey(Payout,null=True,blank=True)
	
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
