from django.db import models

############################################
####### Notification Center ################
############################################

class Notification(models.Model):
	user = models.ForeignKey('account.BasicUser')
	date = models.DateTimeField(auto_now_add=True)
	viewed = models.BooleanField(default=False)

# When buyer messages the seller about an offline item
class SellerMessageNotification(Notification):
	sellermessage = models.ForeignKey('selling.SellerMessage')

# When a seller has a new question
class SellerQuestionNotification(Notification):
	question = models.ForeignKey('questions.Question')

# When a buyer asks a question that is answered
class BuyerQuestionNotification(Notification):
	question = models.ForeignKey('questions.Question')

# When a seller authorizes a buyer to purchase online
class AuthorizedBuyerNotification(Notification):
	item = models.ForeignKey('listing.Item')

# When an item is sold - seller
class SoldNotification(Notification):
	purchaseditem = models.ForeignKey('purchase.PurchasedItem')

# Check payment clears if it is a check
class SoldPaymentNotification(Notification):
	purchaseditem = models.ForeignKey('purchase.PurchasedItem')

class ShippedNotification(Notification):
	purchaseditem = models.ForeignKey('purchase.PurchasedItem')

# When a seller is paid out 
class PayoutNotification(Notification):
	payout = models.ForeignKey('payment.Payout',null=True,blank=True)
	success = models.BooleanField(default=True)

class ReferralNotification(Notification):
	REFERRAL_ACTION = (('buy','buy'),('sell','sell'))
	action = models.CharField(choices=REFERRAL_ACTION,max_length=10)
	referral = models.ForeignKey('account.BasicUser',related_name="notificationreferrer")
