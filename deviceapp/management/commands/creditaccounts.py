from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import *
import balanced
from deviceapp.views_custom import views_email as email_view
from deviceapp.views_general import views_general as email_general
from django.conf import settings
import datetime as datetime
from django.utils.timezone import utc

#########################################################
##### Credits all the Seller's Bank Accounts ############
#########################################################


WAITING_DAYS = 0

class Command(BaseCommand):
    help = 'Credits all the sellers bank accounts'

    def handle(self, *args, **options):
		vetcove_check_count = 0
		vetcove_checkpayout_total = 0
		vetcove_payout_count = 0
		vetcove_payout_total = 0
		bu_set = BasicUser.objects.all() # Iterate over every user in the system
 		#Get all the eligible purchased items
 		for basicuser in bu_set:
 			payout_total = 0
 			commission_total = 0
 			eligiblePurchasedItems = [] #Items for payout
			for p_item in basicuser.purchaseditemseller.all():
				if purchasedItemEligibleForPayout(p_item):
					if not p_item.cartitem.item.commission_paid: 
						commission = general_view.commission(p_item.cartitem.item)
						commission_total += commission
					payout_total += p_item.total-commission
					eligiblePurchasedItems.append(p_item)
			# Continue only if items available for payout
			if eligiblePurchasedItems:
				if basicuser.payout_method == 'none':
					email_view.composeEmailNoPayment(basicuser)
				elif basicuser.payout_method == 'check':
					if basicuser.check_address:	
						check_obj = CheckPayout(user=basicuser,amount=payout_total,address=basicuser.check_address)
						check_obj.save()
						for pi in eligiblePurchasedItems:
							pi.paid_out = True
							pi.payout_method = 'check'
							pi.check = check_obj
							pi.save()
						vetcove_check_count += 1
						vetcove_checkpayout_total += payout_total
						email_view.composeEmailPayoutCheckSent(basicuser,check_obj)
					else:
						email_view.composeEmailNoPayment(basicuser)
				elif basicuser.payout_method == 'bank':
					if basicuser.default_payout_ba:
						try:
							balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
							customer = balanced.Customer.find(basicuser.balanceduri)
							amount = payout_total
							source_uri = basicuser.default_payout_ba.uri
							customer.credit(appears_on_statement_as="Vet Cove",description="Seller Credit",amount=amount,source_uri=source_uri)
							bank_payout_obj = BankPayout(user=basicuser,amount = payout_total,bank_account=basicuser.default_payout_ba)
							bank_payout_obj.save()
							for bpi in eligiblePurchasedItems:
								bpi.paid_out = True
								bpi.payout_method = 'bank'
								bpi.online_payment = bank_payout_obj
								bpi.save()
							vetcove_payout_total += amount/float(100)
							vetcove_payout_count += 1
							email_view.composeEmailPayoutBankSent(basicuser,bank_payout_obj)
						except Exception,e:
							write(self,e)
							email_view.composeEmailPayoutFailed(basicuser,bank_payout_obj)
					else:
						email_view.composeEmailNoPayment(basicuser)
		write(self,"Payouts Complete")
		write(self,"Payout Total: "+str(vetcove_payout_total))
		write(self,"Number of Online Purchases: "+str(vetcove_payout_count))
		write(self,"Check Total: "+str(vetcove_checkpayout_total))
		write(self,"Number of Checks: "+str(vetcove_check_count))		

				
########See if a purchased item is eligible for payout ############
def purchasedItemEligibleForPayout(pitem):
	#First check its been paid out already
	if pitem.paid_out == True:
		return False
	#See if the item has been sent (unsent items don't get paid out)
	if pitem.item_sent == False:
		return False
	#Check if it is been enough time to pay the seller
	now = datetime.datetime.utcnow().replace(tzinfo=utc)
	wait_date = now - datetime.timedelta(days=WAITING_DAYS)
	if pitem.purchase_date > wait_date:
		return False					
 	return True		
	

			
def write(self,string):
	self.stdout.write(str(string))
	return