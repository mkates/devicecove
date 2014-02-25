from django.template import Library

register = Library()

#Condition Quality Text
@register.filter
def condition_quality( value ):
	if value == 1:
		return "A used item that has seen heavy use for its age, or comes with moderate cosmetic or performance-related damage.  The item should be functional and fully able to perform its intended purpose, but may suffer from some decrease in performance due to normal wear and tear including inaccuracy, software lag, decreased readability, or other decrease in performance."
	if value == 2:
		return "A used item that has seen moderate or average use for its age.  It should be fully functional and free of any major defects that would prevent its core purpose from being performed flawlessly.  There may be some minor cosmetic damage, and it may be missing some non-essential accessories or documentation."
	if value == 3:
		return "A used item that has seen very light use in the field. It should be fully functional and free of any defects whatsoever, and should show little-to-no cosmetic signs of wear and tear.  The item may be missing original packaging or accessories, but should function exactly the same as a brand new item."
	if value == 4:
		return "A new, unused item with absolutely no signs of wear. The item may have the manufacturer's seal broken, or the packaging may show slight signs of wear, but the item itself should have never been used in the field except in some cases for light testing or demonstration purposes.  The item may be a factory second or a new, unused item with missing accessories or packaging."
	if value == 5:
		return "A brand-new, unused, unopened, undamaged item sealed in its original manufacturer's packaging.  Packaging should be the same as it would be received directly from the manufacturer or supplier, and sealed by the original manufacturer without any signs of tampering.  The item should carry no noted manufacturer defects, missing accessories or missing documentation.  It must be fully warrantied or eligible for a service contract by the manufacturer."
