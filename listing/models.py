from django.db import models

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
	uses_left = models.IntegerField(max_length=5)
	details = models.CharField(max_length=100) # Short description
	PROMO_TYPE =  (('factor', 'Factor'),('discount', 'Discount'))
	promo_type = models.CharField(max_length = 50,choices=PROMO_TYPE)
	factor = models.IntegerField(max_length=100,null=True,blank=True) # % off commission / 100
	discount = models.IntegerField(max_length = 10,null=True,blank=True) # straight discount
	def __unicode__(self):
		return self.code

### An individual item for sale associated with a product and a user ###
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
	CONTRACT_OPTIONS =  (('warranty', 'Warranty'),('servicecontract', 'Service Contract'),('none', 'None'))
	contract = models.CharField(max_length=40, choices=CONTRACT_OPTIONS,default="none")
	contractdescription = models.TextField(blank=True)
	
	### Condition Type ###
	TYPE_OPTIONS =  (('new', 'New'),('refurbished', 'Refurbished'),('preowned', 'Pre-Owned'))
	conditiontype = models.CharField(max_length=20, choices=TYPE_OPTIONS,default="preowned")
	
	### Condition Quality ###
	CONDITION_OPTIONS =  ((1, 'Functional with Defects'),(2, 'Used Fully Functional'),(3, 'Lightly Used'),(4, 'Like New'),(5, 'Brand New'))
	conditionquality = models.IntegerField(max_length=10,choices=CONDITION_OPTIONS,default=3)
	
	### Descriptions ###
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
	max_price = models.BigIntegerField(max_length=20)
	quantity = models.IntegerField(default=1)
	
	### Payment ###
	promo_code = models.ForeignKey(PromoCode,blank=True,null=True)
	commission_paid = models.BooleanField(default=False)	
	sold_online = models.BooleanField(default=False) # An offline viewable item was bought online
	
	### Miscellaneous ###
	LISTSTATUS_OPTIONS =  (('active', 'Active'),('disabled', 'Disabled'),('incomplete', 'Incomplete'),('sold', 'Sold'),('unsold', 'Not Sold'))
	liststatus = models.CharField(max_length=30,choices=LISTSTATUS_OPTIONS,db_index=True,default='incomplete')
	
	### Charity ###
	charity = models.BooleanField(default=False)
	charity_name = models.ForeignKey(Charity,null=True,blank=True)

	liststage = models.IntegerField(default=0) # Used to track progress through listing an item
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


