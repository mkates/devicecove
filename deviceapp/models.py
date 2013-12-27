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
	
# A product (i.e. Ultrasound XT500), which belongs to a device subcategory
class Product(models.Model):
	name = models.CharField(max_length=150)
	manufacturer = models.ForeignKey(Manufacturer)
	category = models.ForeignKey(SubCategory)
	industries = models.ForeignKey(Industry)
	description = models.TextField()
	def __unicode__(self):
		return self.name
	
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
	return os.path.join('userimages', filename)
def get_file_path_medium(instance, filename):
	ext = filename.split('.')[-1]
	filenamesmall = "%s.%s" % (str(uuid.uuid4())+"_medium", ext)
	return os.path.join('userimages', filename)
		
class Image(models.Model):
	photo = models.ImageField(upload_to=get_file_path_original)
	photo_small = ProcessedImageField(upload_to=get_file_path_small, processors=[ResizeToFit(100, 100)],format='JPEG',options={'quality': 60})
	photo_medium = ProcessedImageField(upload_to=get_file_path_original, processors=[ResizeToFit(500, 500)],format='JPEG',options={'quality': 60})
	id = models.AutoField(primary_key = True)
	
# Generic User already includes email/password
class BasicUser(models.Model):
	user = models.OneToOneField(User)
	businesstype = models.CharField(max_length=60)
	name = models.CharField(max_length=60)
	company = models.CharField(max_length=60)
	email = models.CharField(max_length=60)
	address = models.CharField(max_length=60)
	zipcode = models.IntegerField(max_length=5)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=60)
	website = models.CharField(max_length=60,null=True)
	phonenumber = models.CharField(max_length=60)
			
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
	
	#Asked questions
	def askedQuestionCount(self):
		questions = Question.objects.filter(buyer=self).count()
		return questions
		
	#Get number of unanswered questions
	def savedItemCount(self):
		savedItems = SavedItem.objects.filter(user=self).count()
		return savedItems
	
	#Get number of unanswered questions
	def listedItemCount(self):
		items = Item.objects.filter(user=self).filter(liststatus='active').count()
		return items

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
	savedcount = models.IntegerField()
	liststage = models.IntegerField()
	
	def __unicode__(self):
		return self.name+" from "+self.user.name
		
	# def save(self, *args, **kwargs):
# 		self.subcategory.category.totalunits += 1
# 		self.subcategory.category.save()
# 		self.subcategory.totalunits += 1
# 		self.subcategory.save()
# 		super(Item, self).save(*args, **kwargs)

############################################
####### Images #############################
############################################
class SavedItem(models.Model):
	user = models.ForeignKey(BasicUser)
	item = models.ForeignKey(Item)

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
