from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import *
from deviceapp.views_custom import views_email as email_view
from django.conf import settings
import datetime as datetime
from django.utils.timezone import utc

#########################################################
##### Credits all the Seller's Bank Accounts ############
#########################################################


REMINDER_DAYS= 0

class Command(BaseCommand):
    
    help = 'Updates the count of each category and subcategory'
   
    def handle(self, *args, **options):
    	subcategories = SubCategory.objects.all()
    	for subcategory in subcategories:
    		subcategory.totalunits = subcategory.item_set.filter(liststatus='active').count()
    		subcategory.save()
    	for category in Category.objects.all():
            category.totalunits = 0 
            subcategory_set = category.subcategory_set.all()
            for subcat in subcategory_set:
                category.totalunits += subcat.totalunits
                category.save()
                
def write(self,string):
	self.stdout.write(str(string))
	return
