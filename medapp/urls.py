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

    # Browser Incompatibilities
    url(r'^browser-upgrade','general.views.browserUpgrade'),
    # Password Reset URLS
    url('',include('password_reset.urls')),
    
    ########## General Pages ###############
    #########################################
    url(r'^$','general.views.index'),
    url(r'^error/(?P<errorname>\w+)','general.views.error'),
    url(r'^categories/','general.views.categories'),
    ### Corporate ###
    url(r'^learn/features/','general.views.features'),
    url(r'^learn/supplier/','general.views.supplier'),
    url(r'^learn/manufacturer/','general.views.manufacturer'),
    url(r'^referral/(?P<referral_id>\w+)/','general.views.newReferral'),
    ### Information ###
    url(r'^about/','general.views.about'),
    url(r'^pricing/','general.views.pricing'),
    url(r'^faq/','general.views.faq'),
    url(r'^buyerprotect/','general.views.buyerprotect'),
    url(r'^privacypolicy/','general.views.privacypolicy'),
    url(r'^giveback/','general.views.giveback'),
    url(r'^tos/','general.views.tos'),
    url(r'^contact/','general.views.contact'),
    url(r'^contactform','general.views.contactform'),

    ########## User Portal ##################
    #########################################

    ### Basic Pages ###
    url(r'^new/','account.views.new'),
    url(r'^trending/','account.views.trending'),
    url(r'^deals/','account.views.deals'),
    url(r'^rewards/rewards','account.views.rewardsRewards'),
    url(r'^rewards/store','account.views.rewardsStore'),
    url(r'^rewards/history','account.views.rewardsHistory'),
    url(r'^rewards','account.views.rewardsRewards'),
    url(r'^dashboard','account.views.dashboard'),
    url(r'^account/credits/missions','account.views.creditsMissions'),
    url(r'^account/credits/store','account.views.creditsStore'),
    url(r'^account/credits/history','account.views.creditsHistory'),
    url(r'^account/credits','account.views.creditsMissions'),
    url(r'^account/reviews/history','account.views.reviewsHistory'),
    url(r'^account/reviews/writereview/(?P<reviewid>\w+)','account.views.reviewsWriteReview'),
    url(r'^account/reviews','account.views.reviewsReviews'),
    url(r'^account/questions/answeredquestions','account.views.answeredQuestions'),
    url(r'^account/questions/askedquestions','account.views.askedQuestions'),
    url(r'^account/questions/answerquestion/(?P<questionid>\w+)','account.views.answerQuestion'),
    url(r'^account/questions/askquestion/(?P<productid>\w+)','account.views.askQuestion'),
    url(r'^account/questions/','account.views.askedQuestions'),
    url(r'^account/orders','account.views.orders'),
    url(r'^account/returns','account.views.returns'),
    url(r'^account/analytics','account.views.analytics'),
    url(r'^account/referrals','account.views.referrals'),
    url(r'^account/sell','account.views.sell'),
    url(r'^account/payments','account.views.payments'),
    url(r'^account/settings','account.views.settings'),
    url(r'^account/profile','account.views.profile'),

    url(r'^product/(?P<productname>\w+)','account.views.product'),

    ########## Login ########################
    #########################################
    url(r'^login','account.views.signin'),
    url(r'^form/signupform','account.views.signupform'),
    url(r'^form/loginform','account.views.loginform'),
    url(r'^signin','account.views.signin'),
    url(r'^signup','account.views.signup'),
    url(r'^supplier/signup','account.views.newSupplierSignup'),
    url(r'^form/supplier/signup','account.views.supplierSignupForm'),
    url(r'^newaccount/details','account.views.newAccountDetails'),
    url(r'^newaccount/address','account.views.newAccountAddress'),
    url(r'^newaccount/verification','account.views.newAccountVerification'),
    url(r'^newaccount/tos','account.views.newAccountTOS'),
    url(r'^newaccount/complete','account.views.newAccountComplete'),
    url(r'^newaccount/','account.views.newAccount'),
    url(r'^form/newaccount/details','account.views.newAccountDetailsForm'),
    url(r'^form/newaccount/address','account.views.newAccountAddressForm'),
    url(r'^form/newaccount/verification','account.views.newAccountVerificationForm'),
    url(r'^form/newaccount/tos','account.views.newAccountTOSForm'),
    url(r'^checkemail','account.views.checkemail'),
    url(r'^checkpromo','account.views.checkpromo'),

    ########## Listing ######################
    #########################################
    url(r'^form/autosuggest/','listing.views.autosuggest'),
    #url(r'^form/search','search.views.searchform'),
    url(r'^category/(?P<category>\w+)','listing.views.category'),
    url(r'^manufacturer/(?P<manufacturer>\w+)','listing.views.manufacturer'),
    url(r'^ingredient/(?P<ingredient>\w+)','listing.views.ingredient'),

    ########## Checkout #####################
    #########################################
    url(r'^cart','checkout.views.cart'),

    ########## Seller Portal ################
    #########################################
    url(r'^portal/help','selling.views.portalHelp'),
    url(r'^portal/inventory','selling.views.portalInventory'),
    url(r'^portal/product/(?P<productid>\d+)/edit','selling.views.portalProductEdit'),
    url(r'^portal/product/(?P<productid>\d+)/analytics','selling.views.portalProductAnalytics'),
    url(r'^portal/product/(?P<productid>\d+)/promotions','selling.views.portalProductPromotions'),
    url(r'^portal/product','selling.views.portalProduct'),
    url(r'^portal/purchases','selling.views.portalPurchases'),
    url(r'^portal/purchase/(?P<purchaseid>\d+)','selling.views.portalIndividualPurchase'),
    url(r'^portal/community','selling.views.portalCommunity'),
    url(r'^portal/promotions','selling.views.portalPromotions'),
    url(r'^portal/analytics','selling.views.portalAnalytics'),
    url(r'^portal/account','selling.views.portalAccount'),
    url(r'^portal/reports','selling.views.portalReports'),
    url(r'^portal/dashboard','selling.views.portalDashboard'),
    url(r'^portal/','selling.views.portalDashboard'),













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
    url(r'^checkout/payment/(?P<checkoutid>\d+)','checkout.views.checkoutPayment'),
    url(r'^checkout/review/(?P<checkoutid>\d+)','checkout.views.checkoutReview'),
    url(r'^checkout/confirmation/(?P<orderid>\d+)','checkout.views.checkoutConfirmation'),
    url(r'^newaddress/(?P<checkoutid>\d+)','checkout.views.newAddress'),
    #### Payment Experience
    url(r'^checkout/addcard/(?P<checkoutid>\d+)','checkout.views.checkoutAddCard'),
    #### Complete Checkout  
    url(r'^checkoutpurchase/(?P<checkoutid>\d+)','checkout.views.checkoutPurchase'), 

    ########## Listing App ##################
    #########################################
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


    ########## Account App ##################
    #########################################
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
    url(r'^account/buyhistory','account.views.buyhistory'),
    url(r'^account/sellhistory','account.views.sellhistory'),
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




