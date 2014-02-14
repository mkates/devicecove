from deviceapp.models import *

def basics(request):
	
	#################Cart Calculations ##################
	ci = None
	ci_count = 0
	total = 0
	try: # If accessing as admin there is no BU, so error is thrown
		if request.user.is_authenticated():
			bu = BasicUser.objects.get(user=request.user)
			ci = bu.shoppingcart.cartitem_set.all()		
		else:
			if 'shoppingcart' in request.session:
				sc = ShoppingCart.objects.get(id=request.session['shoppingcart'])
				ci = sc.cartitem_set.all()
		if ci:
			for itm in ci:
				if itm.item.liststatus == 'active':
					total += itm.item.price *itm.quantity
					ci_count += itm.quantity
	################# Shipping Notifications ######################
		itemsToBeShipped = 0
		if request.user.is_authenticated():
			bu = BasicUser.objects.get(user=request.user)
			pis = PurchasedItem.objects.filter(seller=bu)
			for pi in pis:
				if item_paid_for(pi) and not pi.item_sent:
					itemsToBeShipped += 1
				elif pi.item_sent == False:
					itemsToBeShipped += 1
		return {'cart_items':ci,'cart_items_count':ci_count,'cart_total':total,'items_to_be_shipped':itemsToBeShipped}
	except Exception,e:
		print e
		return {}



def item_paid_for(purchaseditem):
	if hasattr(purchaseditem.payment,'checkpayment'):
		if not purchaseditem.payment.checkpayment.received:
			return False
	return True
			