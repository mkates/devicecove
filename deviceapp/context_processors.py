from deviceapp.models import *
from django.core.cache import cache
def basics(request):
	
	#################Cart Calculations ##################
	ci = None
	ci_count = 0
	total = 0
	bu = None
	try:
		if hasattr(request,'user'):
			if request.user.is_authenticated():
				bu = request.user.basicuser
				# Check cache first for cartitems before calling database
				cached_ci = cache.get('cart_items_'+str(bu.id))
				if cached_ci != None:
					ci = cached_ci
				else:
					ci = bu.shoppingcart.cartitem_set.all()	
					cache.set('cart_items_'+str(bu.id),ci)	
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
				# Check cache first for notifications
				cached_notifications = cache.get('notifications_'+str(bu.id))
				if cached_notifications != None:
					notifications = cached_notifications
				else:
					notifications = bu.notification_set.filter(viewed=False)
					cache.set('notifications_'+str(bu.id),notifications)
			return {'cart_items':ci,'cart_items_count':ci_count,'cart_total':total,'notifications':notifications}
		return {}
	except:
		return {}
			