from django.template import Library

register = Library()

#Condition Quality Text
@register.filter
def condition_quality( value ):
	if value == 1:
		return "Items that are not functional as-is, and require manufacturer or third-party refurbishment before they can be used by another practitioner.  These items can be intended as fix-up items by the buyer, or may be used for parts toward other items of the same model."
	if value == 2:
		return "A used item that has seen heavy use (for its age), or comes with moderate cosmetic or performance-related damage.  The item should be functional and fully able to perform its intended purpose, but may suffer from some (inaccuracy, software lag, decreased readability), or decrease in performance ( decrease in performance due to normal wear and tear).  The item must still be usable to other practitioners as is without the need for immediate repair or refurbishing."
	if value == 3:
		return  "A used item that has seen very light use. It should be fully functional and free of any defects whatsoever, and should show little-to-no cosmetic signs of wear and tear.  The item may be missing original packaging or accessories, but should function exactly the same as a brand new item.  Most Very Good items that see regular use are less than one year old."
	if value == 4:
		return "A new, unused item with absolutely no signs of wear. The item may have the manufacturer's seal broken, or the packaging may show slight signs of wear, but the item itself should have never been used except in some cases for light testing (or demonstration)  purposes.  The item may be a factory second or a new, unused item with missing accessories or packaging.";
	if value == 5:
		return "A brand-new, unused, unopened, undamaged item in its original manufacturer's packaging.  Packaging should be the same as it would be received directly from the manufacturer or supplier, and sealed by the original manufacturer without any signs of tampering.";