from django.core.management.base import BaseCommand, CommandError
from helper.credits import *
from account.models import BasicUser

#########################################################
##### Updates Credits for Every User  ###################
#########################################################

class Command(BaseCommand):
    
    help = 'Updates the credits for every user in the system'
   
    def handle(self, *args, **options):
    	for basicuser in BasicUser.objects.all():
            updateCredits(basicuser)
        write(self,"Finished")
                
def write(self,string):
	self.stdout.write(str(string))
	return
