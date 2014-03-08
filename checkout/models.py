from django.db import models
from django.db.models import Q

############################################
####### Checkout Model  ####################
############################################
#### Made up of cart items #################
class Checkout(models.Model):	
	buyer = models.ForeignKey('account.BasicUser')
	shipping_address = models.ForeignKey('account.Address',null=True,blank=True)
	start_time = models.DateTimeField(auto_now_add = True,blank=True)
	payment = models.ForeignKey('payment.Payment',null=True,blank=True)
	
	STATE_OPTIONS =  ((0, 'login'),(1, 'shipping'),(2, 'payment'),(3, 'review'),(4, 'failed_submit'),(5, 'purchased'))
	state = models.IntegerField(max_length=1, choices=STATE_OPTIONS)
	
	# Purchase Details, means successfully charged as well
	purchased = models.BooleanField(default=False)
	purchased_time = models.DateTimeField(null=True,blank=True)
	
	def subtotal(self):
		return sum([cartitem.price*cartitem.quantity for cartitem in self.cartitem_set.all()])
	
	# Get total amount due for this checkout
	def total(self):
		return int(self.subtotal() * (1-self.buyer.bonus/float(10000)))
	
	def bonus_discount(self):
		return self.subtotal()-self.total()
		
	# Number of items in cart
	def numberitems(self):
		return sum([cartitem.quantity for cartitem in self.cartitem_set.all()])

	# Is shipping address required? Items can all be pick-up only
	def shippingAddressRequired(self):
		for cartitem in self.cartitem_set.all():
			print cartitem.item.item_type
			if cartitem.item.item_type == 'PharmaItem':
				return True
			elif not cartitem.item.equipment.shippingincluded:
				return True
		return False

############################################
####### Shopping Cart and Cart Items #######
############################################	

class ShoppingCart(models.Model):
	user = models.OneToOneField('account.BasicUser',null=True,blank=True)
	datecreated = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	
	# Get list of items
	def cart_items(self):
		return [cartitem.item for cartitem in self.cartitem_set.all()]

class CartItem(models.Model):
	checkout = models.ForeignKey(Checkout,null=True,blank=True)
	dateadded = models.DateTimeField(auto_now_add = True)
	item = models.ForeignKey('listing.Item')
	price = models.BigIntegerField() # In case price changes during checkout
	shoppingcart = models.ForeignKey(ShoppingCart,null=True,blank=True)
	quantity = models.IntegerField(default=1,max_length=4)
	message = models.TextField(blank=True)

	# Finds the number of other shopping carts that have this item
	def numbercarts(self):
		return CartItem.objects.filter(~Q(shoppingcart = None)).filter(item=self.item).count()-1
	
	def amount(self):
		return self.item.price*self.quantity