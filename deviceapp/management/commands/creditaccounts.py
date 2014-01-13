from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import *
import balanced
from django.conf import settings
import datetime
from django.utils.timezone import utc

#########################################################
##### Credits all the Seller's Bank Accounts ############
#########################################################

# Need to group payouts into one payment 

class Command(BaseCommand):
    help = 'Credits all the sellers bank accounts'

    def handle(self, *args, **options):
        bas = BankAccount.objects.all()
        balanced.configure(settings.BALANCED_API_KEY)
        for ba in bas:
			bank_account = balanced.BankAccount.find(ba.uri)
			credit = bank_account.credit(amount=1000)
			self.stdout.write(str(credit))
			
		# Step 1. Get all the unpaid, 14 days old, direct deposit payout purchases
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		# Make sure at least 2 weeks pass
		2_weeks_ago = now - timedelta(days=14)
		items = PurchasedItem.objects.filter(paid_out=False).filter(purchase_date__gte=2_weeks_ago)
		for p_item in items:
			# Only if they have a bank account and it is their payment method
			if item.user.payment_option == 'directdeposit':	
				bank_account = balanced.BankAccount.find(p_item.seller.bankaccount.uri)
				credit = bank_account.credit(amount=int(p_item.amount*100),appears_on_statement_as="VetCove")
				
		
		# Step 2. Check all the previous payouts from the last payouts
		# Status can be pending, paid (credits) or succeeded(debits), or failed
			self.stdout.write(str(credit))
		# Step 2. 
	

def timeSincePayout(purchaseditem):
	purchase_time = purchaseditem.