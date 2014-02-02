from django.template import Library

register = Library()

@register.filter
def multiply( value , arg ):
  return int(float(value)*float(arg))

@register.filter
def dividepercent( value , arg ):
  return str(100-int(round(float(value)/float(arg),2)*100))+"%"