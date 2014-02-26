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

def creditSellerAccounts():
		if hasattr(settings,'TESTING'):
			live = True if not settings.TESTING else False
		else:
			live = True
		#Initialize balanced if live
		if live:
			balanced.configure(settings.BALANCED_API_KEY) # Configure Balanced API

		# Finally, check all pending payouts and update accordingly 
		if live:
			checkPendingPayouts()
			
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
					if not p_item.item.commission_paid: 
						commission = p_item.commission
					if p_item.charity:
						charity = int(p_item.total()*.01)
					commission_total += commission
					charity_total += charity
					payout_total += p_item.total()-commission-charity
					eligiblePurchasedItems.append(p_item)
			
			if payout_total > 1500000:
				eligiblePurchasedItems = reducePurchasedItems(eligiblePurchasedItems)
			# Continue only if items available for payout
			if eligiblePurchasedItems:
				if hasattr(basicuser.payout_method,'checkaddress'):
					amount = int(payout_total*(1-CC_PROCESSING_FEE))
					cc_fee = payout_total-amount
					check_obj = CheckPayout(user=basicuser,amount=amount,address=basicuser.payout_method.checkaddress,total_commission=commission_total,cc_fee=cc_fee,total_charity=charity_total)
					check_obj.save()
					for pi in eligiblePurchasedItems:
						pi.paid_out = True
						pi.paid_date = datetime.datetime.utcnow().replace(tzinfo=utc)
						pi.payout = check_obj
						pi.save()
					vetcove_check_count += 1
					vetcove_checkpayout_total += amount
					email_view.composeEmailPayoutSent(basicuser,check_obj)
					notification = PayoutNotification(user=basicuser,payout=check_obj)
					notification.save()
				elif hasattr(basicuser.payout_method,'balancedbankaccount'):
					try:
						bank_payout_obj = None
						amount = int(payout_total*(1-CC_PROCESSING_FEE))
						cc_fee = payout_total-amount
						source_uri = basicuser.payout_method.balancedbankaccount.uri
						if live:
							customer = balanced.Customer.find(basicuser.balanceduri)
							credit = customer.credit(appears_on_statement_as="Vet Cove",description="Seller Credit",amount=amount,source_uri=source_uri)	
							transaction_number = credit.transaction_number
							events_uri = credit.events_uri
						else: # Else is used for testing purposes
							transaction_number = "ABC123"
							events_uri = 'ABC1234'
						bank_payout_obj = BankPayout(user=basicuser,
											amount=amount,
											bank_account=basicuser.payout_method.balancedbankaccount,
											total_commission=commission_total,
											total_charity=charity_total,
											cc_fee=cc_fee, 
											transaction_number=transaction_number,
											events_uri=credit.uri
										)
						bank_payout_obj.save()
						if live:
							if credit.status == 'failed':
								raise Exception("Payout Failed")
						for bpi in eligiblePurchasedItems:
							bpi.paid_out = True
							bpi.paid_date = datetime.datetime.utcnow().replace(tzinfo=utc)
							bpi.payout = bank_payout_obj
							bpi.save()
						vetcove_payout_total += amount
						vetcove_payout_count += 1
						email_view.composeEmailPayoutSent(basicuser,bank_payout_obj)
						notification = PayoutNotification(user=basicuser,payout=bank_payout_obj)
						notification.save()
					except Exception,e:
						print str(basicuser.id)+": "+str(e)
						email_view.composeEmailPayoutFailed(basicuser,basicuser.payout_method,eligiblePurchasedItems)	
						notification = PayoutNotification(user=basicuser,payout=bank_payout_obj,success=False)
						notification.save()
				else:
					email_view.composeEmailNoPayment(basicuser)
					notification = PayoutNotification(user=basicuser,success=False)
					notification.save()

		return {'bank_payout_total':vetcove_payout_total,
			'number_bank':vetcove_payout_count,
			'check_payout_total':vetcove_checkpayout_total,
			'number_check':vetcove_check_count
		}


### Checks all pending payouts, updates successes and failures ###
def checkPendingPayouts():
	for payout in BankPayout.objects.filter(status="pending"):
		credit = balanced.Credit.find('/v1/customers/CU1HCy6qF3ZiHvAc3CrgsM3R/credits/CR1WlvZ6soiOdHlYDrqsPS7u')
		if credit.status == 'failed':
			payout.status = 'failed'
			payout.save()
			purchaseditems = payout.purchaseditem_set.all()
			for pi in purchaseditems:
				pi.paid_out = False
				pi.paid_date = None
				pi.payout_method = None
				pi.save()
			email_view.composeEmailPayoutFailed(payout.user,payout,purchaseditems)	
		if credit.status == 'paid':
			payout.status = 'paid'
			payout.save()
	return

			
########See if a purchased item is eligible for payout ############
def purchasedItemEligibleForPayout(pitem):
	#First check its been paid out already
	if pitem.paid_out == True:
		return False

	# Third, see if the item has been sent (unsent items don't get paid out)
	# Offline items are exempt from this requirement, as well as items that are pick up only 
	if not (pitem.item_sent == True or pitem.item.offlineviewing or not pitem.shipping_included):
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
