from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField

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

class Category(models.Model):
	name = models.CharField(max_length=60)
	displayname = models.CharField(max_length=50)
	industry = models.ForeignKey(Industry)
	totalunits = models.IntegerField()
	def __unicode__(self):
		return self.displayname

class SubCategory(models.Model):
	name = models.CharField(max_length=60,unique=True)
	displayname = models.CharField(max_length=50)
	category = models.ManyToManyField(Category)
	maincategory = models.ForeignKey(Category,related_name='maincategory')
	totalunits = models.IntegerField()
	def __unicode__(self):
		return self.displayname
	
############################################
####### Users Database #####################
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
	filenamemdium = "%s.%s" % (str(uuid.uuid4())+"_medium", ext)
	return os.path.join('userimages', filenamemedium)
		
class Image(models.Model):
	photo = models.ImageField(upload_to=get_file_path_original)
	photo_small = ProcessedImageField(upload_to=get_file_path_small, processors=[ResizeToFit(100, 100)],format='JPEG',options={'quality': 60})
	photo_medium = ProcessedImageField(upload_to=get_file_path_medium, processors=[ResizeToFit(500, 500)],format='JPEG',options={'quality': 60})
	id = models.AutoField(primary_key = True)
	
# Generic User already includes email/password
class BasicUser(models.Model):
	user = models.OneToOneField(User)
	businesstype = models.CharField(max_length=60)
	name = models.CharField(max_length=60)
	company = models.CharField(max_length=60)
	email = models.CharField(max_length=60)
	address_one = models.CharField(max_length=60)
	address_two = models.CharField(max_length=60,null=True,blank=True)
	zipcode = models.IntegerField(max_length=5)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=60)
	website = models.CharField(max_length=60,null=True)
	phonenumber = models.CharField(max_length=60)
	#Balanced customer URI
	balanceduri = models.CharField(max_length=255,null=True,blank=True)
	PAYMENT_OPTIONS =  (('none', 'None'),('check', 'Check'),('directdeposit', 'Direct Deposit'))
	payment_method = models.CharField(max_length=20,choices=PAYMENT_OPTIONS,default='None')
	defaultcard = models.ForeignKey('BalancedCard',null=True,blank=True)
	
	def __unicode__(self):
		return self.user.username
	
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
		
	#Number of unanswered questions
	def wishlist(self):
		savedItems = SavedItem.objects.filter(user=self).count()
		return savedItems
	
	#Get counts for each type of listing
	def listedItemCount(self):
		dict = {'all':0,'sold':0,'inactive':0,'active':0,'incomplete':0,'deleted':0}
		for item in Item.objects.filter(user=self):
			dict[item.liststatus] += 1
			if item.liststatus != 'deleted':
				dict['all'] += 1
		return dict
	
	#Number of purchased items
	def orderhistory(self):
		return PurchasedItem.objects.filter(buyer=self).count()
	
	#Number of sold items
	def sellhistory(self):
		return PurchasedItem.objects.filter(seller=self).count()

#An individual item for sale associated with a product and a user
class Item(models.Model):
	user = models.ForeignKey(BasicUser)
	
	### General Product Information
	name = models.CharField(max_length=200)
	subcategory = models.ForeignKey(SubCategory)
	manufacturer = models.TextField(blank=True)
	
	### Specs
	serialno = models.CharField(max_length=30,null=True,blank=True)
	modelyear = models.IntegerField(max_length=4,null=True,blank=True)
	originalowner = models.BooleanField()
	
	### Warranty + Service Contracts
	CONTRACT_OPTIONS =  (
		('warranty', 'Warranty'),
		('servicecontract', 'Service Contract'),
		('none', 'No Warranty / Service Contract')
	)
	contract = models.CharField(max_length=40, choices=CONTRACT_OPTIONS)
	contractdescription = models.TextField(blank=True)
	
	#Condition/Write-Ins
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
		(4, 'Very Good'),
		(5, 'Like New'),
		(6, 'Brand New')
	)
	conditionquality = models.IntegerField(max_length=10,choices=CONDITION_OPTIONS) #1 being parts only to 6 being brand new
	conditiondescription = models.TextField(blank=True)
	productdescription = models.TextField(blank=True)
	whatsincluded = models.TextField(blank=True)		
	#Shipping and Price
	shippingincluded = models.BooleanField(default=True)
	offlineviewing = models.BooleanField(default=False)
	tos = models.BooleanField(default=False)
	price = models.FloatField(max_length=20)
	
	#Miscellaneous 
	LISTSTATUS_OPTIONS =  (
		('active', 'Active'),
		('inactive', 'Inactive'),
		('incomplete', 'Incomplete'),
		('sold', 'Sold'),
		('deleted', 'Deleted')
	)
	mainimage = models.ForeignKey(Image,null=True,blank=True)
	liststatus = models.CharField(max_length=30, choices=LISTSTATUS_OPTIONS)
	listeddate = models.DateField(auto_now_add = True,blank=True)
	quantity = models.IntegerField(default=1)
	savedcount = models.IntegerField()
	liststage = models.IntegerField()
	
	def __unicode__(self):
		return self.name+" from "+self.user.name

############################################
####### Saved Items ########################
############################################
class SavedItem(models.Model):
	user = models.ForeignKey(BasicUser)
	item = models.ForeignKey(Item)

############################################
####### Images of Items ####################
############################################
class ItemImage(Image):
	item = models.ForeignKey(Item,null=True)
			
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
	question = models.TextField()
	item = models.ForeignKey(Item)
	buyer = models.ForeignKey(BasicUser)
	seller = models.ForeignKey(BasicUser,related_name="seller")
	dateasked = models.DateTimeField(auto_now_add = True,blank=True)
	answer = models.TextField(null=True,blank=True)
	dateanswered = models.DateTimeField(blank=True,null=True)
	
	def __unicode__(self):
		return self.question

############################################
####### Addresses Model  ###################
############################################
class UserAddress(models.Model):
	user = models.ForeignKey(BasicUser)
	name = models.CharField(max_length=50)
	address_one = models.CharField(max_length=100)
	address_two = models.CharField(max_length=100,null=True,blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zipcode = models.IntegerField(max_length=100)
	phonenumber = models.CharField(max_length=100)
	
############################################
####### Shopping Cart ######################
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
	dateadded = models.DateTimeField(auto_now_add = True,blank=True)
	item = models.ForeignKey(Item)
	shoppingcart = models.ForeignKey(ShoppingCart,null=True,blank=True)
	quantity = models.IntegerField(default=1,max_length=3)
	
	def numbercarts(self):
		return CartItem.objects.filter(item=self.item).count()-1

############################################
####### Balanced Models ####################
############################################

#### Balanced Credit Card ##################
class BalancedCard(models.Model):
	user = models.ForeignKey(BasicUser)
	card_uri = models.CharField(max_length=255)
	brand = models.CharField(max_length=100)
	cardhash = models.CharField(max_length=255)
	expiration_month = models.IntegerField(max_length=2)
	expiration_year = models.IntegerField(max_length=4)
	last_four = models.IntegerField(max_length=4)
	datecreated = models.DateTimeField(auto_now_add = True,blank=True)

#### Balanced Bank Account ##################
class BankAccount(models.Model):
	user = models.OneToOneField(BasicUser)
	uri = models.CharField(max_length=255)
	fingerprint = models.CharField(max_length=255)
	bank_name = models.CharField(max_length=255)
	bank_code = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	account_number = models.CharField(max_length=255)
	datecreated = models.DateTimeField(auto_now_add = True,blank=True)

#### Mailing address for checks ###############
class CheckAddress(models.Model):
	user = models.OneToOneField(BasicUser)
	name = models.CharField(max_length=50)
	address_one = models.CharField(max_length=100)
	address_two = models.CharField(max_length=100,null=True,blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zipcode = models.IntegerField(max_length=100)

############################################
####### Checkout Model  ####################
############################################
class Checkout(models.Model):
	cartitem = models.ManyToManyField(CartItem)
	buyer = models.ForeignKey(BasicUser)
	shipping_address = models.ForeignKey(UserAddress,null=True,blank=True)
	start_time = models.DateTimeField(auto_now_add = True,blank=True)
	payment = models.ForeignKey(BalancedCard,null=True,blank=True)
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
	
	#Get total amount due for this checkout
	def total(self):
		total = 0
		cartitems = self.cartitem.all()
		for cartitem in cartitems:
			total += cartitem.item.price*cartitem.quantity
		return int(total)
	
	#Number of items in cart
	def numberitems(self):
		count = 0
		cartitems = self.cartitem.all()
		for cartitem in cartitems:
			count += cartitem.quantity
		return count
	
############################################
### Purchased Items ########################
############################################
# Update item state when creating an instance of PurchasedItem
class PurchasedItem(models.Model):
	seller = models.ForeignKey(BasicUser,related_name="purchaseditem_seller")
	buyer = models.ForeignKey(BasicUser,related_name="purchaseditem_buyer")
	item = models.ForeignKey(Item)
	amount = models.FloatField(max_length=20)
	quantity = models.IntegerField(max_length=6)
	purchase_data = models.DateTimeField(auto_now_add = True)
	# Step 2: Seller sends item
	item_sent = models.BooleanField(default=False)
	item_sent_details = models.TextField(blank=True)
	
	# Did the seller get paid yet?
	paid_out = models.BooleanField(default=False)
	paid_data = models.DateTimeField(null=True,blank=True)





############################################
### Item Reviews ###########################
############################################	
class SellerReview(models.Model):
	seller = models.ForeignKey(BasicUser,related_name="sellerreview_seller")
	buyer = models.ForeignKey(BasicUser,related_name="sellerreview_buyer")
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
	
	
	
	