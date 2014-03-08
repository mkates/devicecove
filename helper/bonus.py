from account.models import *
from purchase.models import *
from general.models import *
import datetime
from django.utils.timezone import utc

##############################################
##### Updates Bonus Amount for a User ########
##############################################
def updateBonus(basicuser):
	# Format [type,reference,quantity,expiration]
	bonuses = []

	# Current date
	now = datetime.datetime.utcnow().replace(tzinfo=utc).now().date()
	
	# First, check referrals 
	bu = BasicUser.objects.filter(referrer=basicuser)
	for ref in bu:
		action_date = firstBuyorSell(ref)
		if action_date:
			bonuses.append(['referral',bu,1,action_date+datetime.timedelta(365)])
	
	# Second, check sold items
	for pi_sold in basicuser.purchaseditemseller.all():
		bonuses.append(['sold',pi_sold,pi_sold.quantity,pi_sold.purchase_date+datetime.timedelta(90)])
	
	# Third, check purchased items
	for pi_buy in basicuser.purchaseditembuyer.all():
		bonuses.append(['buy',pi_buy,pi_buy.quantity,pi_buy.purchase_date+datetime.timedelta(90)])
	
	# Fourth, check feedback
	if basicuser.feedback_set.exists():
		feedback = basicuser.feedback_set.latest('date')
		bonuses.append(['feedback',None,1,feedback.date+datetime.timedelta(365)])

	# Welcome 
	if basicuser.referrer:
		bonuses.append(['welcome',basicuser.referrer,1,basicuser.creation_date+datetime.timedelta(365)])

	active_bonus = []
	inactive_bonus = []
	for bonus in bonuses:
		if bonus[3] < now:
			inactive_bonus.append(bonus)
		else:
			active_bonus.append(bonus)

	total_bonus = sum([min(300,bonus[2]*25) for bonus in active_bonus])
	basicuser.bonus = total_bonus
	basicuser.save()
	return {'active_bonus':active_bonus,'inactive_bonus':inactive_bonus,'total_bonus':total_bonus}

### Finds a basicuser's first purchase or sale, returns None otherwise ###
def firstBuyorSell(basicuser):
	action_date = None
	for seller in basicuser.purchaseditemseller.all():
		if not action_date:
			action_date = seller.purchase_date
		else:
			if action_date > seller.purchase_date:
				action_date = seller.purchase_date
	for buyer in basicuser.purchaseditemseller.all():
		if not action_date:
			action_date = seller.purchase_date
		else:
			if action_date > seller.purchase_date:
				action_date = seller.purchase_date
	return action_date
