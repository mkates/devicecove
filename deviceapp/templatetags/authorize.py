from django.template import Library

register = Library()

@register.filter
def authorize( value , arg, arg_two ):
	return arg