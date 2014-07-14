from checkout.models import *
from django.core.cache import cache
from listing.models import *
def basics(request):
	#################Cart Calculations ##################
	ci = None
	ci_count = 0
	subtotal = 0
	bu = None
	clinic = False
	supplier = False
	if hasattr(request,'user'):
		if request.user.is_authenticated():
			bu = request.user.basicuser
			group_type = bu.group_type()
			if group_type == 'clinic':
				clinic=True
			if group_type == 'supplier':
				supplier = True
	categories = Category.objects.all().prefetch_related('parent')
	maincategories = {}
	for mc in categories.filter(main=True):
		maincategories[mc.id] = {'name':mc.name,'displayname':mc.displayname,'subcat':[]}
	for c in categories:
		if c.parent:
			if c.parent.id in maincategories:
				maincategories[c.parent.id]['subcat'] = maincategories[c.parent.id]['subcat'] + [(c.name,c.displayname)]
	

	return {'categories':categories,'maincategories':maincategories,'basicuser':bu,'clinic':clinic,'supplier':supplier}
			