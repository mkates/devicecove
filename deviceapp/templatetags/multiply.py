from django.template import Library

register = Library()

@register.filter
def multiply( value , arg ):
  return int(value)*int(arg)