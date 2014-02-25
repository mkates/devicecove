from django.test import TestCase
from deviceapp.models import *
from deviceapp.views_custom import payout as payout
from django.conf import settings

class BasicUserTest():
    def setUp(self):
    	# General Models Set Up
        settings.TESTING = True
        
    	self.ind = Industry.objects.create(name='veterinary',displayname='Veterinary')
    	self.cat = Category.objects.create(name='ultrasound',displayname='Ultrasound',industry=self.ind)
    	self.subcat = SubCategory.objects.create(name='ultrasoundprobes',displayname='Ultrasound Probes',maincategory=self.cat)
    	self.subcat.category.add(self.cat)
    	self.subcat.save()

    	# Create Some Users
        self.user_1 = User.objects.create(username="mitch@aim.com", email="mitch@aim.com")
        self.user_2 = User.objects.create(username="bob@aim.com", email="bob@aim.com")
        self.user_3 = User.objects.create(username="joe@aim.com", email="joe@aim.com")
        self.bu_1 = BasicUser.objects.create(user=self.user_1,firstname="Mitch",lastname="Kates",email=self.user_1.email,zipcode=12345)
        self.bu_2 = BasicUser.objects.create(user=self.user_2,firstname="Bob",lastname="Rogers",email=self.user_2.email,zipcode=07722)
        self.bu_3 = BasicUser.objects.create(user=self.user_3,firstname="Joe",lastname="Smith",email=self.user_3.email,zipcode=90012)

        # User Bank Account
        self.bba_1 = BalancedBankAccount.objects.create(user=self.bu_3,uri='ABCDEF',fingerprint='12345',bank_name="Wells Fargo",bank_code="123",
        	name='Joe Smith',account_number='xxxxxxxx1234')
        self.bu_3.payout_method = self.bba_1
        self.bu_3.save()

        # Create Some Items
        self.item_1 = Item.objects.create(user=self.bu_1,name="Ultrasound 1",subcategory=self.subcat,msrp_price=14300,price=8200)
        self.item_2 = Item.objects.create(user=self.bu_2,name="Ultrasound 2",subcategory=self.subcat,msrp_price=15300,price=9200)
        self.item_3 = Item.objects.create(user=self.bu_3,name="Ultrasound 3",subcategory=self.subcat,msrp_price=16300,price=10200)
        self.item_4 = Item.objects.create(user=self.bu_3,name="Ultrasound 4",subcategory=self.subcat,msrp_price=17300,price=11200)
        self.item_5 = Item.objects.create(user=self.bu_3,name="Ultrasound 5",subcategory=self.subcat,msrp_price=18300,price=12200)
        self.item_6 = Item.objects.create(user=self.bu_3,name="Ultrasound 6",subcategory=self.subcat,msrp_price=19300,price=13200)

        # Creae some Purchased Items
        self.order_1 = Order.objects.create(buyer=self.bu_1,total=23400)
        pi_1 = PurchasedItem.objects.create(seller=self.bu_3,buyer=self.bu_1,order=self.order_1,item=self.item_4,quantity=1,unit_price=self.item_4.price,
        	item_name=self.item_4.name,commission=3000,item_sent=True)
        pi_2 = PurchasedItem.objects.create(seller=self.bu_3,buyer=self.bu_1,order=self.order_1,item=self.item_5,quantity=1,unit_price=self.item_5.price,
        	item_name=self.item_5.name,commission=2000,item_sent=True,charity=True)


    def test_generic_bank_payout(self):
    	payout_stats = payout.creditSellerAccounts(False)
    	amount = 23400-5000-int(.01*12200)
    	amount_after_cc = int(amount*.97)
        self.assertEqual(payout_stats['bank_payout_total'], amount_after_cc)
