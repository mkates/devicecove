from django.template import Library

register = Library()

##################################
# Converts int value to dollars ##
##################################
@register.filter
def dollars(value):
	if not value:
		value = '0'
	value = str(int(value))
	value = value.zfill(3)
	dollars = list(value[0:-2])
	for i in range(len(value)-5,0,-3):
		dollars.insert(i,',')
	dollars = "".join(dollars)
	if not dollars:
		dollars = '0'
	return "$"+dollars+'.'+value[-2:]

@register.filter
def percent(value):
	percent = value/float(100)
	if value%100 == 0:
		return int(percent)
	else:
		return percent