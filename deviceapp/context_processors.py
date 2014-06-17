from checkout.models import *
from django.core.cache import cache
from listing.models import *
def basics(request):
	#################Cart Calculations ##################
	ci = None
	ci_count = 0
	subtotal = 0
	bu = None
	if hasattr(request,'user'):
		if request.user.is_authenticated():
			bu = request.user.basicuser
	categories = Category.objects.all()[0:19]
	return {'categories':categories,'basicuser':bu}
			