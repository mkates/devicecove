from deviceapp.models import *

def cart_item(request):
	ci = None
	ci_count = 0
	if request.user.is_authenticated():
		bu = BasicUser.objects.get(user=request.user)
		ci = bu.shoppingcart.cartitem_set.all()
	else:
		if 'shoppingcart' in request.session:
			sc = ShoppingCart.objects.get(id=request.session['shoppingcart'])
			ci = sc.cartitem_set.all()
	if ci:
		ci_count = len(ci)	
	return {'cart_items':ci,'cart_items_count':ci_count }