from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#####################################################################
#########  General ##################################################
#####################################################################
urlpatterns = patterns('',
	#Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #Password Reset
    url('',include('password_reset.urls')),
    
    #General Pages
    url(r'^$','deviceapp.views2.index'),
    url(r'^faq','deviceapp.views2.faq'),
    url(r'^buyerprotect','deviceapp.views2.buyerprotect'),
    url(r'^listintro','deviceapp.views2.listintro'),
    
    #User Actions
    url(r'^imageupload','deviceapp.views2.imageupload'),    
    url(r'^saveitem','deviceapp.views2.saveitem'),
    url(r'^removeitem','deviceapp.views2.removeitem'),
	url(r'^edititem/(?P<itemid>\d+)','deviceapp.views2.edititem'),
	url(r'^editform','deviceapp.views2.editform'),
    url(r'^addproduct','deviceapp.views2.addproduct'),
    url(r'^listproduct','deviceapp.views2.listproduct'),
    url(r'getsubcategories','deviceapp.views2.getsubcategories'),
    url(r'^existingproductcheck','deviceapp.views2.existingproductcheck'),
    url(r'^postitem','deviceapp.views2.postitem'),
    url(r'^messageseller','deviceapp.views2.messageseller'),
    url(r'^askquestion','deviceapp.views2.askquestion'),
    url(r'^deletequestion','deviceapp.views2.deletequestion')
)
#####################################################################
#########  Account ###################################################
#####################################################################

urlpatterns += patterns('',
	url(r'^profile','deviceapp.views2.profile'),
	url(r'^profsettings/(?P<field>\w+)','deviceapp.views2.updateprofsettings'),
    url(r'^usersettings','deviceapp.views2.usersettings'),
    url(r'^listeditems','deviceapp.views2.listeditems'),
    url(r'^saveditems','deviceapp.views2.saveditems'),
    url(r'^logout','deviceapp.views2.logout_view'),
    url(r'^forgotpassword','deviceapp.views2.forgotpassword'),
    url(r'^lgnrequest','deviceapp.views2.lgnrequest'),
    url(r'^login','deviceapp.views2.loginview'),
    url(r'^signup','deviceapp.views2.signup'), 
    url(r'^accounthistory','deviceapp.views2.accounthistory'),
    url(r'^newuserform','deviceapp.views2.newuserform')
)
#####################################################################
#########  Search ###################################################
#####################################################################

urlpatterns += patterns('',
	url(r'^searchquery','deviceapp.views2.searchquery'),
	url(r'^autosuggest','deviceapp.views2.autosuggest'),
	url(r'^customsearch','deviceapp.views2.customsearch'),
	url(r'^productsearch/(?P<industryterm>\w+)/(?P<categoryterm>\w+)/(?P<subcategoryterm>\w+)','deviceapp.views2.productsearch')

)
#####################################################################
#########  Product Pages ############################################
#####################################################################

urlpatterns += patterns('',
	url(r'^item/(?P<itemid>\d+)/details','deviceapp.views2.itemdetails'),
    url(r'^item/(?P<itemid>\d+)/buyingoptions','deviceapp.views2.itemoptions')
)
#####################################################################
#########  Django SES Statistics ####################################
#####################################################################
#urlpatterns += (url(r'^admin/django-ses/', include('django_ses.urls')),)

handler404 = 'deviceapp.views2.my_404_view'
