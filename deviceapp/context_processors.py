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
	################# General Notifications ######################
		notifications = None
		if request.user.is_authenticated():
			bu = BasicUser.objects.get(user=request.user)
			notifications = bu.notification_set.filter(viewed=False)
		return {'cart_items':ci,'cart_items_count':ci_count,'cart_total':total,'notifications':notifications}
	except Exception,e:
		print e
		return {}



def item_paid_for(purchaseditem):
	if hasattr(purchaseditem.payment,'checkpayment'):
		if not purchaseditem.payment.checkpayment.received:
			return False
	return True
			