from django.db import models
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
	name = models.CharField(max_length=40)
	displayname = models.CharField(max_length=50)
	def __unicode__(self):
		return self.displayname

class Category(models.Model):
	name = models.CharField(max_length=60)
	CATEGORY_TYPE =  (('equipment', 'Equipment'),('pharma', 'Pharmaceutical'))
	type = models.CharField(max_length=30,choices=CATEGORY_TYPE, db_index=True,default='equipment')
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

### Used to supplement the medical listings ### (BETA)
class PharmaBase(models.Model):
	name = models.CharField(max_length=100,unique=True)
	mainimage = models.ForeignKey('Image',related_name="medicalitemimage",null=True,blank=True)
	### Include all generic information about a drug here
	uses = models.TextField() # Uses ~! delimiter
	description = models.TextField()


############################################
### Promotional Codes ######################
############################################
class PromoCode(models.Model):
	code = models.CharField(max_length=100,unique=True)
	promo_text = models.CharField(max_length=255) # Fun description
	active = models.BooleanField()
	uses_left = models.IntegerField(max_length=5,default=10000)
	details = models.CharField(max_length=100) # Short description
	PROMO_TYPE =  (('factor', 'Factor'),('discount', 'Discount'))
	promo_type = models.CharField(max_length = 50,choices=PROMO_TYPE)
	factor = models.IntegerField(max_length=100,null=True,blank=True) # % off commission / 100
	discount = models.IntegerField(max_length = 10,null=True,blank=True) # straight discount
	def __unicode__(self):
		return self.code

############################################
### Items ##################################
############################################
class Item(models.Model):
	### Reference to the user ###
	user = models.ForeignKey('account.BasicUser')
	creation_date = models.DateField(auto_now_add=True)

	### Pricing ###
	msrp_price = models.BigIntegerField(max_length=20,null=True,blank=True)
	price = models.BigIntegerField(max_length=20,null=True,blank=True)

	### Is License Required? ###
	vet_license = models.BooleanField(default=False)
	
	### General Product Information ###
	name = models.CharField(max_length=200)
	subcategory = models.ForeignKey(SubCategory,null=True,blank=True)
	manufacturer = models.TextField(blank=True)

	### Promotions ###
	promo_code = models.ForeignKey(PromoCode,blank=True,null=True)

	### Image ###
	mainimage = models.ForeignKey('Image',related_name="mainitemimage",null=True,blank=True)

	### Counts ###
	tos = models.BooleanField(default=False)
	liststage = models.IntegerField(default=0) # Used to track progress through listing an item
	savedcount = models.IntegerField(default=0)
	views = models.IntegerField(default=0) # Counts number of page requests

	### Charity ###
	charity = models.BooleanField(default=False)
	charity_name = models.ForeignKey('general.Charity',null=True,blank=True)

	### List Status ###
	LISTSTATUS_OPTIONS =  (('active', 'Active'),('disabled', 'Disabled'),('incomplete', 'Incomplete'),('sold', 'Sold'),('unsold', 'Not Sold'))
	liststatus = models.CharField(max_length=30,choices=LISTSTATUS_OPTIONS,db_index=True,default='incomplete')
	
	def __unicode__(self):
		return self.name

	def msrp_discount(self):
		return int((self.price-self.msrp_price)/float(self.price)*100)

	def item_type(self):
		if hasattr(self,'equipment'):
			if hasattr(self.equipment,'usedequipment'):
				return 'usedequipment'
			else:
				return 'newequipment'
		else:
			return 'pharmaitem'

	def item_handle(self):
		if hasattr(self,'equipment'):
			if hasattr(self.equipment,'usedequipment'):
				return self.equipment.usedequipment
			else:
				return self.equipment.newequipment
		else:
			return self.pharmaitem

### An individual item for sale associated with a product and a user ###
class Equipment(Item):
	
	### Specs ###
	serialno = models.CharField(max_length=30,null=True,blank=True)
	modelyear = models.IntegerField(max_length=4,null=True,blank=True)
	originalowner = models.BooleanField(default=False)

	### Warranty + Service Contracts ###
	CONTRACT_OPTIONS =  (('warranty', 'Warranty'),('servicecontract', 'Service Contract'),('none', 'None'))
	contract = models.CharField(max_length=40, choices=CONTRACT_OPTIONS,default="none")
	contractdescription = models.TextField(blank=True)
	
	### Descriptions ###
	productdescription = models.TextField(blank=True)
	whatsincluded = models.TextField(blank=True)		
	
	### Logistics ###
	shippingincluded = models.BooleanField(default=True)

	### Commission Structure ###
	COMMISSION_TYPE = (('buy_online','buy_online'),('cpc','cpc'))
	commission_type = models.CharField(max_length=30, choices=COMMISSION_TYPE,default="buy_online")
	
class UsedEquipment(Equipment):

	### Store the highest price ###
	max_price = models.BigIntegerField(max_length=20,default=0)

	### Condition Type ###
	TYPE_OPTIONS =  (('refurbished', 'Refurbished'),('preowned', 'Pre-Owned'))
	conditiontype = models.CharField(max_length=20, choices=TYPE_OPTIONS,default="preowned")
	
	### Condition Quality ###
	CONDITION_OPTIONS =  ((1, 'Functional with Defects'),(2, 'Used Fully Functional'),(3, 'Lightly Used'),(4, 'Like New'),(5, 'Brand New'))
	conditionquality = models.IntegerField(max_length=10,choices=CONDITION_OPTIONS,default=3)
	conditiondescription = models.TextField(blank=True)

	### Commission Object ###
	commission_paid = models.BooleanField(default=False)	
	sold_online = models.BooleanField(default=False) # Was it purchased online?

	### Offline viewing ###
	offlineviewing = models.BooleanField(default=False)

class NewEquipment(Equipment):	
	quantity = models.IntegerField(max_length=5,default=1)

class PharmaItem(Item):
	pharma_base = models.ForeignKey(PharmaBase,blank=True,null=True) #Link to generic pharma information
	quantity = models.IntegerField(max_length=5,default=1)

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
	item = models.ManyToManyField(Item)
	photo = ProcessedImageField(upload_to=get_file_path_original,processors=[ResizeToFit(1300, 1000)],format='JPEG',options={'quality': 60})
	photo_small = ProcessedImageField(upload_to=get_file_path_small, processors=[ResizeToFit(100, 100)],format='JPEG',options={'quality': 60})
	photo_medium = ProcessedImageField(upload_to=get_file_path_medium, processors=[ResizeToFit(500, 500)],format='JPEG',options={'quality': 60})

############################################
### Price Changes  #########################
############################################
# Store all price changes of items #########
class PriceChange(models.Model):
	item = models.ForeignKey(Item)
	date_changed = models.DateTimeField(auto_now_add = True)
	original_price = models.BigIntegerField(max_length = 14)
	new_price = models.BigIntegerField(max_length = 14)

