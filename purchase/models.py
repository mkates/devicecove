from django.db import models

############################################
### Purchased Items  #######################
############################################	

class Order(models.Model):
	buyer = models.ForeignKey('account.BasicUser')
	payment = models.ForeignKey('payment.Payment',null=True,blank=True)
	purchase_date = models.DateTimeField(auto_now_add = True)
	total = models.BigIntegerField(max_length=20)
	tax = models.BigIntegerField(max_length=13,default=0)
	shipping_address = models.ForeignKey('account.Address',null=True,blank=True) # Can be null if pick-up only item
	transaction_number = models.CharField(max_length=40)

class PurchasedItem(models.Model):
	purchase_date = models.DateTimeField(auto_now_add = True)

	# Seller and Buyer
	seller = models.ForeignKey('account.BasicUser',related_name="purchaseditemseller")
	buyer = models.ForeignKey('account.BasicUser',related_name="purchaseditembuyer")
	order = models.ForeignKey(Order)
	
	# Details
	item = models.ForeignKey('listing.Item')
	quantity = models.IntegerField(max_length = 5)
	unit_price = models.BigIntegerField(max_length=20)
	item_name = models.CharField(max_length=300)
	
	# Deductions
	charity = models.BooleanField(default=False)
	charity_name = models.ForeignKey('general.Charity',null=True,blank=True)
	promo_code = models.ForeignKey('listing.PromoCode',null=True,blank=True)
	commission = models.BigIntegerField(max_length=14)

	# Post Purchase
	shipping_included = models.BooleanField(default=True)
	item_sent = models.BooleanField(default=False)
	seller_message = models.TextField(blank=True)
	buyer_message = models.TextField(blank=True)
	
	# Seller Payment
	paid_out = models.BooleanField(default=False)
	paid_date = models.DateTimeField(null=True,blank=True)
	payout = models.ForeignKey('payment.Payout',null=True,blank=True)
	
	def total(self):
		return self.unit_price*self.quantity