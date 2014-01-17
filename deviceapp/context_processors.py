from deviceapp.models import *

def cart_item(request):
	ci = None
	ci_count = 0
	try: # If accessing as admin there is no BU, so error is thrown
		if request.user.is_authenticated():
			bu = BasicUser.objects.get(user=request.user)
			ci = bu.shoppingcart.cartitem_set.all()		
		else:
			if 'shoppingcart' in request.session:
				sc = ShoppingCart.objects.get(id=request.session['shoppingcart'])
				ci = sc.cartitem_set.all()
		if ci:
			ci_count = activeItemCount(ci)
		#Calculate shopping total
		total = 0
		for itm in ci:
			if itm.item.liststatus == 'active':
				total += itm.item.price *itm.quantity
		return {'cart_items':ci,'cart_items_count':ci_count,'cart_total':total }
	except:
		return {}

def activeItemCount(queryset):
	count = 0
	for ci in queryset:
		if ci.item.liststatus == 'active':
			count += 1
	return count