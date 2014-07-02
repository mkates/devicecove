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
	categories = Category.objects.all().prefetch_related('parent')
	maincategories = {}
	for mc in categories.filter(main=True):
		maincategories[mc.id] = {'name':mc.name,'displayname':mc.displayname,'subcat':[]}
	for c in categories:
		if c.parent:
			if c.parent.id in maincategories:
				maincategories[c.parent.id]['subcat'] = maincategories[c.parent.id]['subcat'] + [(c.name,c.displayname)]
	return {'categories':categories,'maincategories':maincategories,'basicuser':bu}
			