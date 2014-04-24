from checkout.models import *
from django.core.cache import cache
def basics(request):
	
	#################Cart Calculations ##################
	ci = None
	ci_count = 0
	subtotal = 0
	bu = None
	if hasattr(request,'user'):
		if request.user.is_authenticated():
			bu = request.user.basicuser
			return {'basicuser':bu}
	return {}
	# 		ci = bu.shoppingcart.cartitem_set.all()	
	# 	if ci:
	# 		for itm in ci:
	# 			if itm.item.liststatus == 'active':
	# 				subtotal += itm.item.price *itm.quantity
	# 				ci_count += itm.quantity
		
	# 	################# General Notifications ######################
	# 	notifications = None
	# 	if request.user.is_authenticated():
	# 		notifications = bu.notification_set.filter(viewed=False)
	# 	return {'cart_items':ci,'cart_items_count':ci_count,'notifications':notifications,'basicuser':bu}
	# return {}
			