from django.template import Library

register = Library()

@register.filter
def phonenumber(value):
    number = str(value)
    formatted_number = "("+number[0:3]+") "+number[3:6]+"-"+number[6:10]
    return formatted_number
