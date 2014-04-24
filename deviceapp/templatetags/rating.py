from django.template import Library

register = Library()

##################################
# Converts rating into text ######
##################################
@register.filter
def ratingtext(value):
	if value < 10:
		return 'Poor'
	elif value < 20:
		return 'Below Average'
	elif value < 30:
		return 'Average'
	elif value < 40:
		return 'Good'
	else:
		return 'Excellent'

@register.filter
def ratingstars(value):
	if value < 15:
		return 15
	elif value < 20:
		return 20
	elif value < 25:
		return 25
	elif value < 30:
		return 30
	elif value < 35:
		return 35
	elif value < 40:
		return 40
	elif value < 45:
		return 45
	else:
		return 50
	