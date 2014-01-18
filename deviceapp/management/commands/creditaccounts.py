from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import *
import balanced
from django.conf import settings
import datetime as datetime
from django.utils.timezone import utc

#########################################################
##### Credits all the Seller's Bank Accounts ############
#########################################################

# Need to group payouts into one payment 

WAITING_DAYS = 0

class Command(BaseCommand):
    help = 'Credits all the sellers bank accounts'

    def handle(self, *args, **options):
		vetcove_payout_total = 0
		vetcove_payout_count = 0
 		bu_set = BasicUser.objects.all() # Iterate over every user in the system
 		#Get all the eligible purchased items
 		for basicuser in bu_set:
 			payout_total = 0
 			eligiblePurchasedItems = [] #Items for payout
			for p_item in basicuser.purchaseditemseller.all():
				if purchasedItemEligibleForPayout(p_item):
					payout_total += p_item.total 
					eligiblePurchasedItems.append(p_item)
		
			# Continue only if items available for payout
			if eligiblePurchasedItems:
				write(self,vetcove_payout_total)
				write(self,vetcove_payout_count)
				if basicuser.payout_method == 'none':
					emailUserNoPayoutMethod(basicuser)
				elif basicuser.payout_method == 'check':
					if basicuser.check_address:	
						check_obj = Check(user=basicuser,amount=payout_total)
						check_obj.save()
						for pi in eligiblePurchasedItems:
							pi.paid_out = True
							pi.payout_method = 'check'
							pi.save()
					else:
						emailUserNoPayoutMethod(basicuser)
				elif basicuser.payout_method == 'bank':
					if basicuser.default_payout_ba:
						try:
							balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
							customer = balanced.Customer.find(basicuser.balanceduri)
							amount = payout_total*100
							source_uri = basicuser.default_payout_ba.uri
							customer.credit(appears_on_statement_as="Vet Cove",description="Seller Credit",amount=amount,source_uri=source_uri)
							for bpi in eligiblePurchasedItems:
								bpi.paid_out = True
								bpi.payout_method = 'bank'
								bpi.save()
							vetcove_payout_total += amount/100
							vetcove_payout_count += 1
						except Exception,e:
							write(self,e)
							emailUserPaymentMethodFailed(basicuser)
					else:
						emailUserNoPayoutMethod(basicuser)
		write(self,"Payouts Complete")
		write(self,"Payout Total: "+str(vetcove_payout_total))
		write(self,"Number of Purchases: "+str(vetcove_payout_count))
			
			
				
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
 
######## No Payment Method Email ##########################	
def emailUserNoPayoutMethod(basicuser):
	write(self,'No Payout Method')
 	return

######## No Payment Method Email ##########################	
def emailUserPaymentMethodFailed(basicuser):
	write(self,'Payment Method Failed')
 	return	
 	
 	
 	
 	
 		# Check payment statuses
#  		for p_item in items:
#  			payment_method = p_item.cartitem.item.user.payment_method
#  			if payment_method == 'none':
#  				##############################
#  				#### Email them about missing payment method
#  				##############################
#  				i = 1
#  			elif payment_method == 'check':
#  				##############################
#  				#### Compile a list for Jamie
#  				##############################
#  				
#  			write(self,payment_method)	
# 				#bank_account = balanced.BankAccount.find(p_item.seller.bankaccount.uri)
# 				#credit = bank_account.credit(amount=int(p_item.amount*100),appears_on_statement_as="VetCove")
# 				i = 1
# 		
# 		# Step 2. Check all the previous payouts from the last payouts
# 		# Status can be pending, paid (credits) or succeeded(debits), or failed
# 			#self.stdout.write(str(credit))
# 		# Step 2. 
# 
# #  bas = BankAccount.objects.all()
# #         balanced.configure(settings.BALANCED_API_KEY)
# #         for ba in bas:
# # 			bank_account = balanced.BankAccount.find(ba.uri)
# # 			credit = bank_account.credit(amount=1000)
# # 			self.stdout.write(str(credit))
# 


			
def write(self,string):
	self.stdout.write(str(string))
	return