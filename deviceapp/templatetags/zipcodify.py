from django.template import Library

register = Library()

@register.filter
def zipcodify(value):
    str_zipcode = str(value)
    return str_zipcode.zfill(5)
