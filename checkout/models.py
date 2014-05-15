from django.db import models
from django.db.models import Q

class ShoppingCart(models.Model):
	creation_date = models.DateTimeField(auto_now_add=True)
	clinic = models.OneToOneField('account.Clinic')
	
	# Get list of items
	def cart_items(self):
		return [cartitem.item for cartitem in self.cartitem_set.all()]

	def summary(self):
		subtotal = sum([cartitem.amount() for cartitem in self.cartitem_set.all()])
		credits = min(subtotal,self.user.credits)
		return {'subtotal':subtotal,'credits':credits,'total':subtotal-credits}

class CartItem(models.Model):
	inventory = models.ForeignKey('listing.Inventory',null=True,blank=True) # Null means they'll take any supplier
	item = models.ForeignKey('listing.Item')
	shoppingcart = models.ForeignKey(ShoppingCart)
	date_added = models.DateTimeField(auto_now_add=True)
	address = models.ForeignKey('account.Address')
	quantity = models.IntegerField(default=1,max_length=4)

	def amount(self):
		return self.inventory.base_price*self.quantity