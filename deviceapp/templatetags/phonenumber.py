from django.template import Library

register = Library()

@register.filter
def phonenumber(value):
	if value == None:
		return ''
	else:
		number = str(value)
		number = number.replace("(",'').replace(")",'').replace("-",'').replace(" ",'')
		formatted_number = "("+number[0:3]+") "+number[3:6]+"-"+number[6:10]
		return formatted_number
