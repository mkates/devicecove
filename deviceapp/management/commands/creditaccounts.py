from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import *
import balanced
from deviceapp.views_custom import payout as payout_view
from django.conf import settings
import datetime as datetime
from django.utils.timezone import utc

#########################################################
##### Credits all the Seller's Bank Accounts ############
#########################################################

class Command(BaseCommand):
    help = 'Credits all the sellers bank accounts'
    args = '<type>'

    def handle(self, *args, **options):
    	live = False
    	for type in args:
    		if type.lower() == 'live':
    			live = True
		results = payout_view.creditSellerAccounts(live)
					
		write(self,"Payouts Complete")
		write(self,"Bank Payout Total: $"+str(results['bank_payout_total']))
		write(self,"Number Bank Payouts: $"+str(results['number_bank']))
		write(self,"Check Payout Total: $"+str(results['check_payout_total']))
		write(self,"Number Check Payouts: $"+str(results['number_check']))

				
########See if a purchased item is eligible for payout ############
def purchasedItemEligibleForPayout(pitem):
	#First check its been paid out already
	if pitem.paid_out == True:
		return False

	#Second check if the item was paid for by a check and we haven't received the check yet
	if hasattr(pitem.order.payment,'checkpayment'):
		if not pitem.order.payment.checkpayment.received:
			return False

	# Third, See if the item has been sent (unsent items don't get paid out)
	# Offline items are exempt from this requirementm, as well as items that are pick up only 
	if not (pitem.item_sent == True or pitem.cartitem.item.offlineviewing or not pitem.shipping_included):
		return False

	# Fourth, check if it is been enough time to pay the seller
	now = datetime.datetime.utcnow().replace(tzinfo=utc)
	wait_date = now - datetime.timedelta(days=WAITING_DAYS)
	if pitem.purchase_date > wait_date:
		return False					
 	return True	

##### Remove Items until under $15K ##############
def reducePurchasedItems(pitems):
	new_pitems = pitems
	while total > 1500000:
		new_pitems.pop()
		total = totalPayout(new_pitems)
	return new_pitems

def totalPayout(pitems):
	total = 0
	for pitem in pitems:
		total += pitem.total*pitem.quantity
	return total
	
##### Writing Helper Function ############		
def write(self,string):
	self.stdout.write(str(string))
	return