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
    url(r'^$','deviceapp.views.index'),
    url(r'^faq','deviceapp.views.faq'),
    url(r'^buyerprotect','deviceapp.views.buyerprotect'),
    url(r'^listintro','deviceapp.views.listintro'),
    
    #User Actions
    url(r'^imageupload','deviceapp.views.imageupload'),    
    url(r'^saveitem','deviceapp.views.saveitem'),
    url(r'^removeitem','deviceapp.views.removeitem'),
	url(r'^edititem/(?P<itemid>\d+)','deviceapp.views.edititem'),
	url(r'^editform','deviceapp.views.editform'),
    url(r'^addproduct','deviceapp.views.addproduct'),
    url(r'^listproduct','deviceapp.views.listproduct'),
    url(r'^existingproductcheck','deviceapp.views.existingproductcheck'),
    url(r'^postitem','deviceapp.views.postitem')
)
#####################################################################
#########  Account ###################################################
#####################################################################

urlpatterns += patterns('',
	url(r'^profile','deviceapp.views.profile'),
	url(r'^profsettings/(?P<field>\w+)','deviceapp.views.updateprofsettings'),
    url(r'^settings','deviceapp.views.settings'),
    url(r'^listeditems','deviceapp.views.listeditems'),
    url(r'^saveditems','deviceapp.views.saveditems'),
    url(r'^logout','deviceapp.views.logout_view'),
    url(r'^forgotpassword','deviceapp.views.forgotpassword'),
    url(r'^lgnrequest','deviceapp.views.lgnrequest'),
    url(r'^login','deviceapp.views.loginview'),
    url(r'^signup','deviceapp.views.signup'), 
    url(r'^accounthistory','deviceapp.views.accounthistory'),
    url(r'^newuserform','deviceapp.views.newuserform'),url(r'^newuserform','deviceapp.views.newuserform')
)
#####################################################################
#########  Search ###################################################
#####################################################################

urlpatterns += patterns('',
	url(r'^searchquery','deviceapp.views.searchquery'),
	url(r'^autosuggest','deviceapp.views.autosuggest'),
	url(r'^customsearch','deviceapp.views.customsearch'),
	url(r'^productsearch/(?P<industryterm>\w+)/(?P<categoryterm>\w+)/(?P<subcategoryterm>\w+)','deviceapp.views.productsearch')

)
#####################################################################
#########  Product Pages ############################################
#####################################################################

urlpatterns += patterns('',
	url(r'^item/(?P<itemid>\d+)/details','deviceapp.views.itemdetails'),
    url(r'^item/(?P<itemid>\d+)/buyingoptions','deviceapp.views.itemoptions')
)
#####################################################################
#########  Django SES Statistics ####################################
#####################################################################
urlpatterns += (url(r'^admin/django-ses/', include('django_ses.urls')),)
