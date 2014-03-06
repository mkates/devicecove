from account.models import *
from purchase.models import *
from general.models import *

##############################################
##### Updates Bonus Amount for a User ########
##############################################
def updateBonus(basicuser):
	# First, check referrals 
	referral_bonus = 0
	bu = BasicUser.objects.filter(referral=basicuser)
	for ref in bu:
		if ref.purchaseditemseller_set.all().exists() or ref.purchaseditembuyer_set.all().exists():
			referral_bonus += 25
	# Second, check sold items
	sold_bonus = 0
	for pi_sold in bu.purchaseditemseller_set.all():
		sold_bonus += 25*pi_sold.quantity
	# Third, check purchased items
	buy_bonus = 0
	for pi_buy in bu.purchaseditemseller_set.all():
		buy_bonus += 25*pi_buy.quantity
	# Fourth, check feedback
	feedback_bonus = 0
	if Contact.filter(user=bu).exists():
		feedback_bonus = 25
	total_bonus = min(300,referral_bonus)+min(300,sold_bonus)+min(300,buy_bonus)+feedback_bonus
	bu.bonus = total_bonus
	bu.save()
	return