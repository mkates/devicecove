from django.test import TestCase
import emails.views as email
from django.conf import settings
from helper.model_imports import *

class BasicUserTest(TestCase):
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
        self.address = Address.objects.create(name="Bob Jones",address_one='1 Main Street',city="Knoxville",state="TN",zipcode=12345,phonenumber=1234567890)
        self.ca_1 = CheckAddress.objects.create(user=self.bu_3,address=self.address)
        self.bu_3.payout_method = self.ca_1
        self.bu_3.save()

        # Create Some Items
        self.item_1 = NewEquipment.objects.create(user=self.bu_1,name="Ultrasound 1",subcategory=self.subcat,msrp_price=14300,price=8200)
        self.item_2 = UsedEquipment.objects.create(user=self.bu_2,name="Ultrasound 2",subcategory=self.subcat,msrp_price=15300,price=9200)
        self.item_3 = NewEquipment.objects.create(user=self.bu_3,name="Ultrasound 3",subcategory=self.subcat,msrp_price=16300,price=10200)
        self.item_4 = NewEquipment.objects.create(user=self.bu_3,name="Ultrasound 4",subcategory=self.subcat,msrp_price=17300,price=11200)
        self.item_5 = NewEquipment.objects.create(user=self.bu_3,name="Ultrasound 5",subcategory=self.subcat,msrp_price=18300,price=12200)
        self.item_6 = NewEquipment.objects.create(user=self.bu_3,name="Ultrasound 6",subcategory=self.subcat,msrp_price=19300,price=13200)

        # Question
        self.question_1 = Question.objects.create(buyer=self.bu_1,seller=self.bu_2,item=self.item_1,question="Is the item still available?")

        self.sellermessage_1 = SellerMessage.objects.create(buyer=self.bu_1,item=self.item_1,name="John Doe",email="johndoe@aim.com",phone=1234567890,message="New Contact Message",reason='Offline Visit')
        self.comm_obj = Commission.objects.create(item=self.item_1,price=12345,amount=1234,payment=self.bba_1,transaction_number='12345')
        
        # Create some Purchased Items
        self.order_1 = Order.objects.create(buyer=self.bu_1,item_total=23400,credits=1000,transaction_number="123454")
        self.pi_1 = PurchasedItem.objects.create(seller=self.bu_3,buyer=self.bu_1,order=self.order_1,item=self.item_4,quantity=1,unit_price=self.item_4.price,
        	item_name=self.item_4.name,commission=3000,item_sent=True)
        self.pi_2 = PurchasedItem.objects.create(seller=self.bu_3,buyer=self.bu_1,order=self.order_1,item=self.item_5,quantity=1,unit_price=self.item_5.price,
        	item_name=self.item_5.name,commission=2000,item_sent=True,charity=True)

        #Payout object
        self.payout_1 = CheckPayout.objects.create(user = self.bu_3,amount=20123,total_commission =8254,total_charity = 1124,cc_fee = 3122,address=self.ca_1)
   
    def test_generic_bank_payout(self):
    	payout_stats = creditSellerAccounts()
    	amount = 23400-5000-int(.01*12200) # Original - commission - charity
    	amount_after_cc = int(amount*.97) # - processing_fee
        self.assertEqual(payout_stats['check_payout_total'], amount_after_cc)

    def test_emails(self):
        ### Make sure they don't throw any errors ###
        email.composeEmailWelcome(self.bu_1)
        email.composeEmailPVP(self.bu_1)
        email.composeEmailListingConfirmation(self.bu_1,self.item_1)
        email.composeEmailNewQuestion(self.bu_1,self.question_1)
        email.composeEmailQuestionAnswered(self.question_1)
        email.composeEmailContactMessage_Seller(self.bu_1,self.sellermessage_1)
        email.composeEmailCommissionCharged(self.bu_1,self.comm_obj)
        email.composeEmailItemSold_Seller(self.bu_1,self.pi_1)
        email.composeEmailItemPurchased_Buyer(self.bu_1,self.order_1)
        email.composeEmailItemShipped_Buyer(self.bu_1,self.pi_1)
        email.composeEmailPayoutSent(self.bu_3,self.payout_1)
        email.composeEmailNoPayment(self.bu_1)
        email.composeEmailPayoutFailed(self.bu_3,self.bba_1,[self.pi_1,self.pi_2])
        email.composeEmailPayoutUpdated(self.bu_3)
        email.composeEmailAuthorizedBuyer(self.item_1,self.bu_2)
        #html_email = email.composeEmailItemPurchased_Buyer(request,request.user.basicuser,Order.objects.get(id=1))
        self.assertEqual(1,1)


        
