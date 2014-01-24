from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import *
from deviceapp.views_custom import views_email as email_view
from django.conf import settings
import datetime as datetime
from django.utils.timezone import utc
import random
import string
#########################################################
##### Credits all the Seller's Bank Accounts ############
#########################################################


REMINDER_DAYS= 0

class Command(BaseCommand):
    
    help = 'Sends email reminders 1 week after contact message to offline, unsold items'
   
    def handle(self, *args, **options):
    	#Grab all active, offline items
		eligibleItems = Item.objects.filter(liststatus="active").filter(offlineviewing=True)
		for item in eligibleItems:
			messages = item.sellermessage_set.all()
			for message in messages:
				if messageShouldSend(message):
					token = generateToken()
					rt = ReminderToken(contact_message=message,token=token)
					write(self,rt)
					rt.save()
					email_view.composeEmailContactMessageFollowUp_Seller(message,token)
					write(self,'Email Sent')
			
def write(self,string):
	self.stdout.write(str(string))
	return

def messageShouldSend(message):
	now = datetime.datetime.utcnow().replace(tzinfo=utc)
	wait_date = now - datetime.timedelta(days=REMINDER_DAYS)
	if  message.date_sent > wait_date: # Check if enough time has passed
		return False
	if ReminderToken.objects.filter(contact_message = message).exists(): # If followup email not already sent
		return False
	return True
	
	
def generateToken():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))