from django.db import models

############################################
####### Payment Models #####################
############################################

class Payment(models.Model):
	user = models.ForeignKey('account.BasicUser',null=True,blank=True)
	datecreated = models.DateTimeField(auto_now_add=True)
	
#### Payment/Payout by Check ##################
class CheckAddress(Payment):
	address = models.ForeignKey('account.Address')

#### Balanced Credit Card ##################
class BalancedCard(Payment):
	uri = models.CharField(max_length=255)
	brand = models.CharField(max_length=100)
	cardhash = models.CharField(max_length=255)
	expiration_month = models.IntegerField(max_length=2)
	expiration_year = models.IntegerField(max_length=4)
	last_four = models.IntegerField(max_length=4)

#### Balanced Bank Account ##################
class BalancedBankAccount(Payment):
	uri = models.CharField(max_length=255)
	fingerprint = models.CharField(max_length=255)
	bank_name = models.CharField(max_length=255)
	bank_code = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	account_number = models.CharField(max_length=255)

############################################
### Payout Record Keeping ##################
############################################

class Payout(models.Model):
	user = models.ForeignKey('account.BasicUser')
	amount = models.BigIntegerField(max_length=20)
	date = models.DateTimeField(auto_now_add = True)
	total_commission = models.BigIntegerField(max_length=20)
	total_charity = models.BigIntegerField(max_length=20)
	cc_fee = models.BigIntegerField(max_length=20)
	
	def subtotal(self):
		return self.amount+self.total_commission+self.cc_fee+self.total_charity
	
#### Record of the bank payout ##################
class BankPayout(Payout):
	bank_account = models.ForeignKey(BalancedBankAccount)
	STATUS_OPTIONS =  (('failed', 'Failed'),('pending', 'Pending'),('paid', 'Paid'))
	status = models.CharField(max_length=20,choices=STATUS_OPTIONS,default='pending')
	transaction_number = models.CharField(max_length=30)
	events_uri = models.CharField(max_length=200)
		
#### Record of the check payout ##################
class CheckPayout(Payout):
	address = models.ForeignKey(CheckAddress)
	sent = models.BooleanField(default=False)

############################################
####### Commission #########################
############################################

class Commission(models.Model):
	item = models.OneToOneField('listing.Item')
	price = models.BigIntegerField(max_length=12) #Price of the item
	amount = models.BigIntegerField(max_length=20) #Commission amount
	payment = models.ForeignKey(Payment) # Can only be a card or bank account
	date = models.DateTimeField(auto_now_add = True)
	transaction_number = models.CharField(max_length=40)
