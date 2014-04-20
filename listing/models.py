from django.db import models
import uuid, os
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField

############################################
####### Product Database Models ############
############################################

# Industries in our case can be small animal, bovine, equine #
class Industry(models.Model):
	name = models.CharField(max_length=40)
	displayname = models.CharField(max_length=50)
	def __unicode__(self):
		return self.displayname

class Manufacturer(models.Model):
	name = models.CharField(max_length=40)
	displayname = models.CharField(max_length=50)
	image = models.ForeignKey('Image',null=True,blank=True)
	totalunits = models.IntegerField(default=0) # Script updates this
	members = models.ManyToManyField('account.BasicUser') # Certain users can edit the product pages of these products
	def __unicode__(self):
		return self.displayname

############ Categories ####################

class Category(models.Model):
	name = models.CharField(max_length=60)
	displayname = models.CharField(max_length=50)
	totalunits = models.IntegerField(default=0) # Script updates this
	def __unicode__(self):
		return self.displayname
 
class MainCategory(Category):
	industry = models.ManyToManyField(Industry)

class SecondCategory(Category):
	category = models.ManyToManyField(MainCategory)
	maincategory = models.ForeignKey(Category,related_name='second_maincategory') # Need a main category for breadcrumbs

class ThirdCategory(models.Model):
	secondcategory = models.ForeignKey(SecondCategory)

############################################
############ Catalog #######################
############################################

### Product Listing (what search is based around) ###
class Product(models.Model):
	name = models.CharField(max_length=200, unique=True)
	category = models.ForeignKey(Category)
	description = models.TextField()
	mainimage = models.ForeignKey('Image',null=True,blank=True)

class Pharma(Product):
	rx = models.BooleanField(default=True)
	compendium = models.CharField(max_length=200)
	human_label = models.BooleanField(default=False)
	ingredient = models.ManyToManyField('Ingredient',null=True,blank=True)

class Needles(Product):
	type = models.CharField(max_length=20)
	length = models.IntegerField(max_length=5) #inches
	wound_support = models.CharField(max_length=10)
	colors = models.ManyToManyField('Color')

class Equipment(Product): # Small equipment items
	details = models.TextField(max_length=100)

class Device(Product): # Large devices
	features = models.TextField() # !~ is the delimiter
	modelyear = models.IntegerField(max_length=4,null=True,blank=True)
	### Warranty + Service Contracts ###
	CONTRACT_OPTIONS =  (('warranty', 'Warranty'),('servicecontract', 'Service Contract'),('none', 'None'))
	contract = models.CharField(max_length=40, choices=CONTRACT_OPTIONS,default="none")
	contractdescription = models.TextField(blank=True)

############################################
####### Man # Specific #####################
############################################

### Item's are products with multiple types, i.e. 50mg and 100mg versions
class Item(models.Model):
	product = models.ForeignKey(Product)
	manufacturer = models.TextField(blank=True)
	manufacturer_no = models.CharField(max_length=25,null=True,blank=True)
	size = models.CharField(max_length=50,null=True,blank=True) # ie. .5kg, 60ml
	unit = models.CharField(max_length=50,null=True,blank=True) # ie. jar, bottle, paste
	itemimage = models.ForeignKey('Image',related_name="itemimage",null=True,blank=True) # if size specific image is available

### What a distributor/manufacturer uploads (their inventory) ###
class Listing(models.Model): 
	sku = models.CharField(max_length=25,null=True,blank=True) # The uploader's SKU for this product
	item = models.ForeignKey(Item)
	supplier = models.ForeignKey('account.Supplier')
	unit_quantity = models.IntegerField(max_length=8) # ie. a case of 12 or a pallet of 144
	quantity_available = models.IntegerField(max_length=8) # Quantity of this amount available
	price = models.BigIntegerField(max_length=13) # in cents

### Tags are used for connecting products outside of traditional category tiers ###
### I.E. Super discount, recent listing, mobile vet, etc. ###
class Tags(models.Model):
	name = models.CharField(max_length=50)
	products = models.ManyToManyField(Product)
### Helper Classes for Product Listings ###
class Ingredient(models.Model):
	name = models.CharField(max_length=50)
class Color(models.Model):
	name = models.CharField(max_length=50)

############################################
### Products ###############################
############################################
class UsedEquipment(models.Model):
	### Reference to the user ###
	user = models.ForeignKey('account.BasicUser')
	creation_date = models.DateField(auto_now_add=True)

	### Pricing ###
	msrp_price = models.BigIntegerField(max_length=20,null=True,blank=True)
	price = models.BigIntegerField(max_length=20,null=True,blank=True)

	### General Product Information ###
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category,null=True,blank=True)
	manufacturer = models.ForeignKey(Manufacturer,null=True,blank=True)

	### Image ###
	mainimage = models.ForeignKey('Image',null=True,blank=True)

	### Counts ###
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
	item = models.ForeignKey(Product)
	photo = ProcessedImageField(upload_to=get_file_path_original,processors=[ResizeToFit(1300, 1000)],format='JPEG',options={'quality': 60})
	photo_small = ProcessedImageField(upload_to=get_file_path_small, processors=[ResizeToFit(100, 100)],format='JPEG',options={'quality': 60})
	photo_medium = ProcessedImageField(upload_to=get_file_path_medium, processors=[ResizeToFit(500, 500)],format='JPEG',options={'quality': 60})

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

