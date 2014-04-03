from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
from djrill import DjrillAdminSite
admin.site = DjrillAdminSite()
admin.autodiscover()

#####################################################################
#########  General ##################################################
#####################################################################
urlpatterns = patterns('',

	####### Admin and Staff URLS ############
    #########################################
	url(r'^staff/overview/(?P<type>\w+)','staffportal.views.staffOverview'),
	url(r'^staff/overview','staffportal.views.staffOverviewForward'),
    url(r'^staff/markassent','staffportal.views.staffMarkAsSent'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Password Reset URLS
    url('',include('password_reset.urls')),
    
    ########## General Pages ###############
    #########################################
    url(r'^$','general.views.index'),
    url(r'^error/(?P<errorname>\w+)','general.views.error'),
    url(r'^faq/','general.views.faq'),
    url(r'^privacypolicy/','general.views.privacypolicy'),
    url(r'^giveback/','general.views.giveback'),
    url(r'^tos/','general.views.tos'),
    url(r'^about/','general.views.about'),
    url(r'^sell/','general.views.sell'),
    url(r'^commission/','general.views.commissionpage'),
    url(r'^pvp/','general.views.pvp'),
    url(r'^buyerprotect/','general.views.buyerprotect'),
    url(r'^listintro/','general.views.listintro'),
    url(r'^equipmentcategories/','general.views.equipmentcategories'),
    url(r'^pharmacategories/','general.views.pharmacategories'),
    url(r'^shop/','general.views.shop'),
    url(r'^buy/','general.views.shop'),
    url(r'^contact/','general.views.contact'),
    url(r'^contactform','general.views.contactform'),
    url(r'^referral/(?P<referral_id>\w+)/','general.views.newReferral'),
    
    ########## Seller Portal ################
    #########################################
    url(r'^seller/','selling.views.sellerHome'),




    ########## Questions App ################
    #########################################
    url(r'^account/buyerquestions','questions.views.buyerquestions'),
    url(r'^account/sellerquestions','questions.views.sellerquestions'),
    url(r'^askquestion','questions.views.askquestion'),
    url(r'^deletequestion','questions.views.deletequestion'),
    url(r'^answerquestion/(?P<questionid>\d+)','questions.views.answerquestion'),

    ########## Checkout  App ################
    #########################################
    url(r'^cart','checkout.views.cart'),
    url(r'^updatecart/wishlist/(?P<cartitemid>\d+)','checkout.views.updateCartWishlist'),
    url(r'^updatecart/delete/(?P<cartitemid>\d+)','checkout.views.updateCartDelete'),
    url(r'^updatecart/quantity/(?P<cartitemid>\d+)','checkout.views.updateCartQuantity'),
    url(r'^addtocart/(?P<itemid>\d+)','checkout.views.addToCart'),
    url(r'^checkout/verify/(?P<error>\w+)','checkout.views.checkoutVerifyError'),
    url(r'^checkout/verify','checkout.views.checkoutVerify'),
    url(r'^checkout/shipping/(?P<checkoutid>\d+)','checkout.views.checkoutShipping'),
    url(r'^checkout/payment/(?P<checkoutid>\d+)','checkout.views.checkoutPayment'),
    url(r'^checkout/review/(?P<checkoutid>\d+)','checkout.views.checkoutReview'),
    url(r'^checkout/confirmation/(?P<orderid>\d+)','checkout.views.checkoutConfirmation'),
    url(r'^checkoutlogin','checkout.views.checkoutlogin'),
    url(r'^useaddress','checkout.views.useAddress'),
    url(r'^newaddress/(?P<checkoutid>\d+)','checkout.views.newAddress'),
    url(r'^deleteaddress','checkout.views.deleteAddress'),
    #### Payment Experience
    url(r'^checkout/addcard/(?P<checkoutid>\d+)','checkout.views.checkoutAddCard'),
    url(r'^checkout/deletepayment/(?P<checkoutid>\d+)/(?P<paymentid>\d+)','checkout.views.checkoutDeletePayment'),
    url(r'^checkout/usepayment/(?P<checkoutid>\d+)/(?P<paymentid>\d+)','checkout.views.checkoutUsePayment'),
    #### Complete Checkout  
    url(r'^checkoutpurchase/(?P<checkoutid>\d+)','checkout.views.checkoutPurchase'), 

    ########## Listing App ##################
    #########################################
    url(r'^getsubcategories','listing.views.getsubcategories'),
    url(r'^newlisting/(?P<listingtype>\w+)','listing.views.newlisting'),
    url(r'^list/business/(?P<itemid>\d+)','listing.views.listbusiness'),
    url(r'^savebusiness/(?P<itemid>\d+)','listing.views.savebusiness'),
    url(r'^list/describe/(?P<itemid>\d+)','listing.views.listitemdescribe'),
    url(r'^list/details/(?P<itemid>\d+)','listing.views.listitemdetails'),
    url(r'^list/photos/(?P<itemid>\d+)','listing.views.listitemphotos'),
    url(r'^list/logistics/(?P<itemid>\d+)','listing.views.listitemlogistics'),
    url(r'^list/preview/(?P<itemid>\d+)','listing.views.listitempreview'),
    url(r'^savedescribe/(?P<itemid>\d+)','listing.views.savedescribe'),
    url(r'^savedetails/(?P<itemid>\d+)','listing.views.savedetails'),
    url(r'^savelogistics/(?P<itemid>\d+)','listing.views.savelogistics'),
    url(r'^list/activate/(?P<itemid>\d+)','listing.views.activateListing'),
    url(r'^list/markassold/(?P<itemid>\d+)','listing.views.markAsSold'),
    url(r'^deletelisting/(?P<itemid>\d+)','listing.views.deleteListing'),
    url(r'^promocode/(?P<itemid>\d+)','listing.views.addPromoCode'),
    url(r'^list/tos/(?P<itemid>\d+)','listing.views.tosListing'), 
    ### Handling Photos
    url(r'^post/imageupload/(?P<itemid>\d+)','listing.views.imageupload'), 
    url(r'^post/deleteimage','listing.views.deleteimage'),  
    url(r'^post/setmainimage','listing.views.setmainimage'), 
    ### Item
    url(r'^item/(?P<itemid>\d+)/details','listing.views.itemdetails'),

    ########## Account App ##################
    #########################################
    url(r'^account/profile','account.views.profile'),
    url(r'^account/notifications','account.views.notifications'),
    url(r'^account/clearnotifications','account.views.clearNotifications'),
    url(r'^account/bonus/','account.views.bonus'),
    url(r'^account/feedback/','account.views.feedback'),
    url(r'^account/feedbackform','account.views.feedbackForm'),
    url(r'^account/feedbackthanks','account.views.feedbackThanks'),
    url(r'^account/referral/','account.views.referral'),
    url(r'^account/referralform','account.views.referralForm'),
    url(r'^account/referralthanks','account.views.referralThanks'),
    url(r'^account/bonushistory','account.views.bonusHistory'),
    url(r'^account/updategeneral','account.views.updateGeneralSettings'),
    url(r'^account/updateseller','account.views.updateSellerSettings'),
    url(r'^account/updatepassword','account.views.updatePassword'),
    url(r'^account/updatenotification','account.views.updateNotification'),
    url(r'^account/updatesettings/newsletter','account.views.updatesettingsnewsletter'),
    url(r'^account/updatesettings/delete','account.views.deleteAccount'),
    url(r'^account/payouthistory','account.views.payoutHistory'),
    url(r'^account/usersettings','account.views.usersettings'),
    url(r'^account/updateproviders','account.views.updateProviders'),
    url(r'^account/listings/(?P<listingtype>\w+)','account.views.listings'),
    url(r'^account/wishlist','account.views.wishlist'),
    url(r'^account/contactmessages','account.views.contactMessages'),
    url(r'^account/payment','account.views.payment'),
    url(r'^account/addcreditcard','account.views.addCreditCard'),
    url(r'^account/addbankaccount','account.views.addBankAccount'),
    url(r'^logout','account.views.logout_view'),
    url(r'^forgotpassword','account.views.forgotpassword'),
    url(r'^lgnrequest','account.views.lgnrequest'),
    url(r'^login','account.views.loginview'),
    url(r'^account/buyhistory','account.views.buyhistory'),
    url(r'^account/sellhistory','account.views.sellhistory'),
    url(r'^newuserform','checkout.views.newuserform'),
    url(r'^checkemail','account.views.checkemail'),
    url(r'^saveitem','account.views.saveitem'),
    url(r'^removeitem','account.views.removeitem'),
    ### Listing in the account
    url(r'^account/editlisting/inactive/(?P<itemid>\d+)','account.views.editListingInactive'),
    url(r'^account/editlisting/active/(?P<itemid>\d+)','account.views.editListingActive'),
    url(r'^account/editlisting/relist/(?P<itemid>\d+)','account.views.editListingRelist'),

    ########## Selling App ##################
    #########################################
    # Post Purchase Experience
    url(r'^purchasesellermessage/(?P<purchaseditemid>\d+)','selling.views.purchasesellermessage'),
    url(r'^account/purchaseshippinginfo/(?P<purchaseditemid>\d+)','selling.views.purchaseshippinginfo'),
    url(r'^account/reportproblem/(?P<purchaseditemid>\d+)','selling.views.reportproblem'),
    url(r'^account/reportproblemform/(?P<purchaseditemid>\d+)','selling.views.reportproblemform'),
    # Post Contact Experience
    url(r'^account/messages/(?P<itemid>\d+)','selling.views.buyermessages'),
    url(r'^account/newcard_chargecommission/(?P<itemid>\d+)','selling.views.newcard_chargecommission'),
    url(r'^account/newbank_chargecommission/(?P<itemid>\d+)','selling.views.newbank_chargecommission'),
    url(r'^gatepayment/(?P<paymentid>\d+)/(?P<itemid>\d+)','selling.views.gatePayment'),
    url(r'^authorizebuyer/(?P<buyerid>\d+)/(?P<itemid>\d+)','selling.views.authorizeBuyer'),
    url(r'^deauthorizebuyer/(?P<buyerid>\d+)/(?P<itemid>\d+)','selling.views.deauthorizeBuyer'),
    # Reminder Token
    url(r'^account/updatelisting/(?P<action>\w+)/(?P<token>\w+)','selling.views.updateListingState'),
    
    ########## Payment App ##################
    #########################################
    url(r'^account/makedefaultpayment/(?P<id>\d+)','payment.views.makeDefaultPayment'),
    url(r'^account/makedefaultpayout/(?P<id>\d+)','payment.views.makeDefaultPayout'),
    url(r'^account/deletepayment/(?P<id>\d+)','payment.views.accountDeletePayment'),
    url(r'^account/addmailingaddress','payment.views.addMailingAddress'),
    url(r'^account/deletemailingaddress/(?P<addressid>\d+)','payment.views.deleteMailingAddress'),

    ########## Search App  ##################
    #########################################
    url(r'^searchquery','search.views.searchquery'),
    url(r'^autosuggest','search.views.autosuggest'),
    url(r'^customsearch','search.views.customsearch'),
    url(r'^productsearch/(?P<industryterm>\w+)/(?P<categoryterm>\w+)/(?P<subcategoryterm>\w+)','search.views.productsearch'),
 
)
#####################################################################
#########  Django Error Handling ####################################
#####################################################################

handler404 = 'general.views.my_404_view'
handler500 = 'general.views.my_500_view'

#####################################################################
#########  Django Debug Toolbar  ####################################
#####################################################################
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )




