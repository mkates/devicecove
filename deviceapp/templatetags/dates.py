import datetime
from django.utils.timezone import utc
from django.template import Library

register = Library()

#Calculates day since value
@register.filter
def days_since( value ):
  now = datetime.datetime.utcnow().replace(tzinfo=utc)
  now = now.date()
  days = now-value
  return days.days
  