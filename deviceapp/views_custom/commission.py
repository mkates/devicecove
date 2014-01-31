#################################################
############# Commission ########################
#################################################

# Calculate commission amount:
# Commission Structure
# Under $20 15%
# $20-$50   14%
# $50-$200  13%
# $200-$500 12%
# $500-2,000 10%
# $2,000+     9%
def commissionPercentage(total_price):
	if total_price < 2000:
		commission = .15
	elif total_price < 5000:
		commission = .14
	elif total_price < 20000:
		commission = .13
	elif total_price < 50000:
		commission = .12
	elif total_price < 200000:
		commission = .10
	else:
		commission = .09
	return commission

######## Amount Saved in commission for a given item #############
def commissionSavings(item):
	start_commission = commissionPercentage(item.price)
	end_commission = commission(item)
	return abs(start_commission-end_commission)

######## Original Item Commission ########################
def originalCommission(item):
	return int(item.price*commissionPercentage(item.price))

######## Get commission of an item ########################	
def commission(item):
	if not item.promo_code:
		return int(item.price*commissionPercentage(item.price))
	elif item.promo_code.promo_type == 'factor':
		return int((item.price*commissionPercentage(item.price)*((item.promo_code.factor)/float(100))))
	elif item.promo_code.promo_type == 'discount':
		return int(max(0,item.price*commissionPercentage(item.price)-item.promo_code.discount))
	return int(item.price*commissionPercentage(item.price))


# I create an object because it is easier to only have one template for emails
# and i want the no_payment_email to mimic the payment_sent_emails
class Payment(object):
    pass

######## Purchased Item Commission Values ##################	
def getStatsFromPurchasedItems(pitem_list):	
	subtotal = 0
	comm = 0
	for pi in pitem_list:
		comm += purchaseditemCommission(pi)
		subtotal += pi.total
	cc_fee = int((subtotal-comm)*.03)
	payment = Payment()
	payment.amount = subtotal-cc_fee-comm
	payment.cc_fee = cc_fee
	payment.subtotal = subtotal
	payment.total_commission = comm
	return payment

######## PurchasedItem Commission ########################
# Need separate method in case price changes on the item, we need to use the purchased item price
def purchaseditemCommission(pitem):
	item = pitem.cartitem.item
	quantity = pitem.quantity
	if not item.promo_code:
		return int(pitem.unit_price*commissionPercentage(pitem.unit_price))*quantity
	elif item.promo_code.promo_type == 'factor':
		return int((pitem.unit_price*commissionPercentage(pitem.unit_price)*((item.promo_code.factor)/float(100))))*quantity
	elif item.promo_code.promo_type == 'discount':
		return int(max(0,pitem.unit_price*commissionPercentage(pitem.unit_price)-item.promo_code.discount))*quantity
	return int(pitem.unit_price*commissionPercentage(pitem.unit_price))*quantity
	