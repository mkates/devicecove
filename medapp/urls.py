from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^',include('password_reset.urls')),
    url(r'^$','deviceapp.views.index'),
    url(r'^imageupload','deviceapp.views.imageupload'),
    url(r'^searchquery','deviceapp.views.searchquery'),
    url(r'^autosuggest','deviceapp.views.autosuggest'),
    url(r'^saveitem','deviceapp.views.saveitem'),
    url(r'^removeitem','deviceapp.views.removeitem'),
	url(r'^edititem/(?P<itemid>\d+)','deviceapp.views.edititem'),
	url(r'^editform','deviceapp.views.editform'),
    url(r'^productsearch/(?P<industryterm>\w+)/(?P<devicecategoryterm>\w+)','deviceapp.views.productsearch'),
    url(r'^login','deviceapp.views.loginview'),
    url(r'^signup','deviceapp.views.signup'),
    url(r'^addproduct','deviceapp.views.addproduct'),
    url(r'^listintro','deviceapp.views.listintro'),
    url(r'^listproduct','deviceapp.views.listproduct'),
    url(r'^forgotpassword','deviceapp.views.forgotpassword'),
    url(r'^lgnrequest','deviceapp.views.lgnrequest'),
    url(r'^logout','deviceapp.views.logout_view'),
    url(r'^saveditems','deviceapp.views.saveditems'),
    url(r'^profile','deviceapp.views.profile'),
    url(r'^settings','deviceapp.views.settings'),
    url(r'^listeditems','deviceapp.views.listeditems'),
    url(r'^postitem','deviceapp.views.postitem'),
    url(r'^accounthistory','deviceapp.views.accounthistory'),
    url(r'^newuserform','deviceapp.views.newuserform'),
    url(r'^item/(?P<itemid>\d+)/details','deviceapp.views.itemdetails'),
    url(r'^item/(?P<itemid>\d+)/buyingoptions','deviceapp.views.itemoptions'),
    url(r'^profsettings/(?P<field>\w+)','deviceapp.views.updateprofsettings'),
    url(r'^customsearch','deviceapp.views.customsearch'),
     url(r'^faq','deviceapp.views.faq'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += (url(r'^admin/django-ses/', include('django_ses.urls')),)