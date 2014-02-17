from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import *
import balanced
from deviceapp.views_custom import views_email as email_view
from deviceapp.views_custom import commission as commission_view
from django.conf import settings
import datetime as datetime
from django.utils.timezone import utc

#########################################################
##### Credits all the Seller's Bank Accounts ############
#########################################################


WAITING_DAYS = 0
CC_PROCESSING_FEE = 0.03

class Command(BaseCommand):
    help = 'Credits all the sellers bank accounts'

    def handle(self, *args, **options):
    	
    	#Initialize balanced
    	#balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API
    	
    	# Counts for Internal Purposes
		vetcove_check_count = 0
		vetcove_checkpayout_total = 0
		vetcove_payout_count = 0
		vetcove_payout_total = 0

 		# Iterate through users, get all the eligible purchased items
 		for basicuser in BasicUser.objects.all():
 			payout_total = 0
 			commission_total = 0
 			charity_total = 0
 			eligiblePurchasedItems = [] # Items for payout
			for p_item in basicuser.purchaseditemseller.all():
				if purchasedItemEligibleForPayout(p_item):
					# If the commission hasn't already been paid i.e. offline items
					commission = 0
					charity = 0
					if not p_item.cartitem.item.commission_paid: 
						commission = commission_view.purchaseditemCommission(p_item)
						charity = int(p_item.total*.01)
						commission_total += commission
						charity_total += charity
					payout_total += p_item.total-commission-charity
					eligiblePurchasedItems.append(p_item)
					
			# Continue only if items available for payout
			if eligiblePurchasedItems:
				if hasattr(basicuser.payout_method,'checkaddress'):
					cc_fee = int(payout_total*CC_PROCESSING_FEE)
					amount = payout_total-cc_fee
					check_obj = CheckPayout(user=basicuser,amount=amount,address=basicuser.payout_method.checkaddress.address,total_commission=commission_total,cc_fee=cc_fee,total_charity=charity_total)
					check_obj.save()
					for pi in eligiblePurchasedItems:
						pi.paid_out = True
						pi.paid_date = datetime.datetime.utcnow().replace(tzinfo=utc)
						pi.payout = check_obj
						pi.save()
					vetcove_check_count += 1
					vetcove_checkpayout_total += amount
					email_view.composeEmailPayoutCheckSent(basicuser,check_obj)
					notification = PayoutNotification(user=basicuser,payout=check_obj)
					notification.save()
				elif hasattr(basicuser.payout_method,'balancedbankaccount'):
					try:
						#customer = balanced.Customer.find(basicuser.balanceduri)
						cc_fee = int(payout_total*CC_PROCESSING_FEE)
						amount = payout_total-cc_fee
						source_uri = basicuser.default_payout_ba.uri
						#customer.credit(appears_on_statement_as="Vet Cove",description="Seller Credit",amount=amount,source_uri=source_uri)
						bank_payout_obj = BankPayout(user=basicuser,cc_fee=cc_fee, amount=amount,bank_account=basicuser.default_payout_ba,total_commission=commission_total,total_charity=charity_total)
						bank_payout_obj.save()
						for bpi in eligiblePurchasedItems:
							bpi.paid_out = True
							bpi.paid_date = datetime.datetime.utcnow().replace(tzinfo=utc)
							bpi.payout = bank_payout_obj
							bpi.save()
						vetcove_payout_total += amount
						vetcove_payout_count += 1
						email_view.composeEmailPayoutBankSent(basicuser,bank_payout_obj)
						notification = PayoutNotification(payout=bank_payout_obj)
						notification.save()
					except Exception,e:
						write(self,str(basicuser.id)+": "+str(e))
						email_view.composeEmailPayoutFailed(basicuser,bank_payout_obj)	
						notification = PayoutNotification(user=basicuser,payout=bank_payout_obj,success=False)
						notification.save()
				else:
					email_view.composeEmailNoPayment(basicuser)
					notification = PayoutNotification(user=basicuser,success=False)
					notification.save()
					
		write(self,"Payouts Complete")
		write(self,"Online Payout Total: $"+str(vetcove_payout_total/float(100)))
		write(self,"Number of Online Purchases: "+str(vetcove_payout_count))
		write(self,"Check Total: $"+str(vetcove_checkpayout_total/float(100)))
		write(self,"Number of Checks: "+str(vetcove_check_count))		

				
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
	

			
def write(self,string):
	self.stdout.write(str(string))
	return