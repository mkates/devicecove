from django.conf.urls import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from djrill import DjrillAdminSite
admin.site = DjrillAdminSite()
admin.autodiscover()

#####################################################################
#########  General ##################################################
#####################################################################
urlpatterns = patterns('',

    #Temporarily, please delete
    url(r'^testemail/','deviceapp.views_custom.testemail'),
	#Admin
	url(r'^staff/overview/(?P<type>\w+)','deviceapp.views_custom.staffOverview'),
	url(r'^staff/overview','deviceapp.views_custom.staffOverviewForward'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^staff/markassent','deviceapp.views_custom.staffMarkAsSent'),
    url(r'^staff/markasreceived','deviceapp.views_custom.staffMarkAsReceived'),
    
    #Password Reset
    url('',include('password_reset.urls')),
    
    #General Pages
    url(r'^$','deviceapp.views_custom.index'),
    url(r'^error/(?P<errorname>\w+)','deviceapp.views_custom.error'),
    url(r'^faq/','deviceapp.views_custom.faq'),
    url(r'^privacypolicy/','deviceapp.views_custom.privacypolicy'),
    url(r'^giveback/','deviceapp.views_custom.giveback'),
    url(r'^tos/','deviceapp.views_custom.tos'),
    url(r'^about/','deviceapp.views_custom.about'),
    url(r'^shop/','deviceapp.views_custom.shop'),
    url(r'^commission/','deviceapp.views_custom.commissionpage'),
    url(r'^pvp/','deviceapp.views_custom.pvp'),
    url(r'^buyerprotect/','deviceapp.views_custom.buyerprotect'),
    url(r'^listintro','deviceapp.views_custom.listintro'),
    url(r'^categories','deviceapp.views_custom.categories'),
    url(r'^buy/','deviceapp.views_custom.buy'),
    #User Actions
    url(r'^imageupload/(?P<itemid>\d+)','deviceapp.views_custom.imageupload'), 
    url(r'^deleteimage','deviceapp.views_custom.deleteimage'),  
    url(r'^setmainimage','deviceapp.views_custom.setmainimage'),   
    url(r'^saveitem','deviceapp.views_custom.saveitem'),
    url(r'^removeitem','deviceapp.views_custom.removeitem'),
    url(r'^listproduct/(?P<subcategory>\w+)','deviceapp.views_custom.listproduct'),
    url(r'getsubcategories','deviceapp.views_custom.getsubcategories'),
    url(r'^existingproductcheck','deviceapp.views_custom.existingproductcheck'),
    url(r'^messageseller/(?P<itemid>\d+)','deviceapp.views_custom.messageseller'),
    url(r'^askquestion','deviceapp.views_custom.askquestion'),
    url(r'^deletequestion','deviceapp.views_custom.deletequestion'),
    url(r'^answerquestion/(?P<questionid>\d+)','deviceapp.views_custom.answerquestion'),
    
    
    #Listing and edit listing pages
    url(r'^list/business/(?P<itemid>\d+)','deviceapp.views_custom.listbusiness'),
    url(r'^savebusiness/(?P<itemid>\d+)','deviceapp.views_custom.savebusiness'),
    url(r'^list/describe/(?P<itemid>\d+)','deviceapp.views_custom.listitemdescribe'),
    url(r'^list/details/(?P<itemid>\d+)','deviceapp.views_custom.listitemdetails'),
    url(r'^list/photos/(?P<itemid>\d+)','deviceapp.views_custom.listitemphotos'),
    url(r'^list/logistics/(?P<itemid>\d+)','deviceapp.views_custom.listitemlogistics'),
    url(r'^list/preview/(?P<itemid>\d+)','deviceapp.views_custom.listitempreview'),
    url(r'^savedescribe/(?P<itemid>\d+)','deviceapp.views_custom.savedescribe'),
    url(r'^savedetails/(?P<itemid>\d+)','deviceapp.views_custom.savedetails'),
	url(r'^savelogistics/(?P<itemid>\d+)','deviceapp.views_custom.savelogistics'),
    url(r'^list/activate/(?P<itemid>\d+)','deviceapp.views_custom.activateListing'),
    url(r'^list/markassold/(?P<itemid>\d+)','deviceapp.views_custom.markAsSold'),
    url(r'^deletelisting/(?P<itemid>\d+)','deviceapp.views_custom.deleteListing'),
    url(r'^promocode/(?P<itemid>\d+)','deviceapp.views_custom.addPromoCode'),
    url(r'^list/tos/(?P<itemid>\d+)','deviceapp.views_custom.tosListing'),
    #Listing in the account
    url(r'^account/editlisting/inactive/(?P<itemid>\d+)','deviceapp.views_custom.editListingInactive'),
    url(r'^account/editlisting/active/(?P<itemid>\d+)','deviceapp.views_custom.editListingActive'),
    url(r'^account/editlisting/relist/(?P<itemid>\d+)','deviceapp.views_custom.editListingRelist'),
    
    #Email Reminder Token Link
    url(r'^account/updatelisting/(?P<action>\w+)/(?P<token>\w+)','deviceapp.views_custom.updateListingState'),
    
    
    #Checkout Experience
    
    url(r'^cart','deviceapp.views_custom.cart'),
    url(r'^updatecart/wishlist/(?P<cartitemid>\d+)','deviceapp.views_custom.updateCartWishlist'),
    url(r'^updatecart/delete/(?P<cartitemid>\d+)','deviceapp.views_custom.updateCartDelete'),
    url(r'^updatecart/quantity/(?P<cartitemid>\d+)','deviceapp.views_custom.updateCartQuantity'),
    url(r'^addtocart/(?P<itemid>\d+)','deviceapp.views_custom.addToCart'),
    url(r'^checkout/verify/(?P<error>\w+)','deviceapp.views_custom.checkoutVerifyError'),
    url(r'^checkout/verify','deviceapp.views_custom.checkoutVerify'),
    url(r'^checkout/shipping/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutShipping'),
    url(r'^checkout/payment/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutPayment'),
    url(r'^checkout/review/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutReview'),
    url(r'^checkout/confirmation/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutConfirmation'),
    
    url(r'^checkoutlogin','deviceapp.views_custom.checkoutlogin'),
    url(r'^useaddress','deviceapp.views_custom.useAddress'),
    url(r'^newaddress/(?P<checkoutid>\d+)','deviceapp.views_custom.newAddress'),
    url(r'^deleteaddress','deviceapp.views_custom.deleteAddress'),
    # Payment Experience
    url(r'^checkout/addcard/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutAddCard'),
    url(r'^checkout/deletepayment/(?P<checkoutid>\d+)/(?P<paymentid>\d+)','deviceapp.views_custom.checkoutDeletePayment'),
    url(r'^checkout/usepayment/(?P<checkoutid>\d+)/(?P<paymentid>\d+)','deviceapp.views_custom.checkoutUsePayment'),
    
    # Review Experience
    url(r'^checkoutmovetosaved/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutMoveToSaved'),
    url(r'^checkoutdeleteitem/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutDeleteItem'),
    url(r'^checkoutchangequantity/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutChangeQuantity'),
    #Complete Checkout  
    url(r'^checkoutpurchase/(?P<checkoutid>\d+)','deviceapp.views_custom.checkoutPurchase') 
)
#####################################################################
#########  Account ###################################################
#####################################################################

urlpatterns += patterns('',
	url(r'^account/profile','deviceapp.views_custom.profile'),
    url(r'^account/notifications','deviceapp.views_custom.notifications'),
	url(r'^account/updategeneral','deviceapp.views_custom.updateGeneralSettings'),
	url(r'^account/updateseller','deviceapp.views_custom.updateSellerSettings'),
	url(r'^account/updatepassword','deviceapp.views_custom.updatePassword'),
    url(r'^account/updatenotification','deviceapp.views_custom.updateNotification'),
    url(r'^account/updatesettings/newsletter','deviceapp.views_custom.updatesettingsnewsletter'),
     url(r'^account/updatesettings/delete','deviceapp.views_custom.deleteAccount'),
    url(r'^account/payouthistory','deviceapp.views_custom.payoutHistory'),
    url(r'^account/usersettings','deviceapp.views_custom.usersettings'),
    url(r'^account/listings/(?P<listingtype>\w+)','deviceapp.views_custom.listings'),
    url(r'^account/wishlist','deviceapp.views_custom.wishlist'),
    url(r'^account/payment','deviceapp.views_custom.payment'),
    url(r'^logout','deviceapp.views_custom.logout_view'),
    url(r'^forgotpassword','deviceapp.views_custom.forgotpassword'),
    url(r'^lgnrequest','deviceapp.views_custom.lgnrequest'),
    url(r'^login','deviceapp.views_custom.loginview'),
    url(r'^account/buyerquestions','deviceapp.views_custom.buyerquestions'),
    url(r'^account/sellerquestions','deviceapp.views_custom.sellerquestions'),
    url(r'^account/buyhistory','deviceapp.views_custom.buyhistory'),
    url(r'^account/sellhistory','deviceapp.views_custom.sellhistory'),
    url(r'^newuserform','deviceapp.views_custom.newuserform'),
    url(r'^checkemail','deviceapp.views_custom.checkemail'),
    
    #Payment
    url(r'^account/addcreditcard','deviceapp.views_custom.addCreditCard'),
    url(r'^account/addbankaccount','deviceapp.views_custom.addBankAccount'),
    url(r'^account/makedefaultpayment/(?P<id>\d+)','deviceapp.views_custom.makeDefaultPayment'),
    url(r'^account/makedefaultpayout/(?P<id>\d+)','deviceapp.views_custom.makeDefaultPayout'),
    url(r'^account/deletepayment/(?P<id>\d+)','deviceapp.views_custom.accountDeletePayment'),
    url(r'^account/addmailingaddress','deviceapp.views_custom.addMailingAddress'),
    url(r'^account/deletemailingaddress/(?P<addressid>\d+)','deviceapp.views_custom.deleteMailingAddress'),
    
    #Post Payment Experience
    url(r'^purchasesellermessage/(?P<purchaseditemid>\d+)','deviceapp.views_custom.purchasesellermessage'),
    url(r'^account/purchaseshippinginfo/(?P<purchaseditemid>\d+)','deviceapp.views_custom.purchaseshippinginfo'),
    url(r'^account/reportproblem/(?P<purchaseditemid>\d+)','deviceapp.views_custom.reportproblem'),
    url(r'^account/reportproblemform/(?P<purchaseditemid>\d+)','deviceapp.views_custom.reportproblemform'),
     
    #Viewing people who have contacted you
    url(r'^account/messages/(?P<itemid>\d+)','deviceapp.views_custom.buyermessages'),
    url(r'^account/newcard_chargecommission/(?P<itemid>\d+)','deviceapp.views_custom.newcard_chargecommission'),
    url(r'^account/newbank_chargecommission/(?P<itemid>\d+)','deviceapp.views_custom.newbank_chargecommission'),
    url(r'^gatepayment/(?P<paymenttype>\w+)/(?P<paymentid>\d+)/(?P<itemid>\d+)','deviceapp.views_custom.gatePayment'),
    url(r'^authorizebuyer/(?P<buyerid>\d+)/(?P<itemid>\d+)','deviceapp.views_custom.authorizeBuyer'),
    url(r'^deauthorizebuyer/(?P<buyerid>\d+)/(?P<itemid>\d+)','deviceapp.views_custom.deauthorizeBuyer')
    
)
#####################################################################
#########  Search ###################################################
#####################################################################

urlpatterns += patterns('',
	url(r'^searchquery','deviceapp.views_custom.searchquery'),
	url(r'^autosuggest','deviceapp.views_custom.autosuggest'),
	url(r'^customsearch','deviceapp.views_custom.customsearch'),
	url(r'^productsearch/(?P<industryterm>\w+)/(?P<categoryterm>\w+)/(?P<subcategoryterm>\w+)','deviceapp.views_custom.productsearch')

)
#####################################################################
#########  Product Pages ############################################
#####################################################################

urlpatterns += patterns('',
	url(r'^item/(?P<itemid>\d+)/details','deviceapp.views_custom.itemdetails')
)
#####################################################################
#########  Django SES Statistics ####################################
#####################################################################

handler404 = 'deviceapp.views_custom.my_404_view'
handler500 = 'deviceapp.views_custom.my_500_view'

#####################################################################
#########  Django Debug Toolbar  ####################################
#####################################################################
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
urlpatterns += patterns('', 
    url(r'', include('fresh.urls'))
)




