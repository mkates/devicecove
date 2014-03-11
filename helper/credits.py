from account.models import *
from purchase.models import *
from general.models import *
import datetime
from django.utils.timezone import utc

##############################################
##### Updates Bonus Amount for a User ########
##############################################
def updateCredits(basicuser):
	# Format [type,reference,quantity]
	credit_list  = []
	pending_credit_list = []
	used_credit_list = []
	credits_earned = 0
	credits_used = 0
	
	# First, check referrals 
	bu = BasicUser.objects.filter(referrer=basicuser)
	for ref in bu:
		action_date = firstBuyorSell(ref)
		if action_date:
			credit_list.append(['referral',ref,1000,action_date])
			credits_earned += 1000
		else:
			pending_credit_list.append(['referral',ref,0])
	
	# Second, check sold items
	for pi_sold in basicuser.purchaseditemseller.all():
		commission_credit = int(.2*pi_sold.commission)
		credit_list.append(['sold',pi_sold,commission_credit,pi_sold.purchase_date])
		credits_earned += commission_credit

	# Third, check feedback
	if basicuser.feedback_set.exists():
		feedback = basicuser.feedback_set.latest('date')
		credit_list.append(['feedback',None,100,feedback.date])
		credits_earned += 100
	
	# Welcome 
	if basicuser.referrer:
		credit_list.append(['welcome',basicuser.referrer,1000,basicuser.creation_date])
		credits_earned += 1000

	# Now find the number of credits used
	for order in basicuser.order_set.all():
		used_credit_list.append(order)
		credits_used += order.credits

	basicuser.credits = credits_earned-credits_used
	basicuser.save()

	return {'credit_list':credit_list,'pending_credit_list':pending_credit_list,'used_credit_list':used_credit_list,'credits_available':credits_earned-credits_used,'credits_earned':credits_earned,'credits_used':credits_used}

### Finds a basicuser's first purchase or sale, returns None otherwise ###
def firstBuyorSell(basicuser):
	action_date = None
	for buyer in basicuser.purchaseditembuyer.all():
		if not action_date:
			action_date = buyer.purchase_date
		else:
			if action_date > buyer.purchase_date:
				action_date = buyer.purchase_date
	return action_date
