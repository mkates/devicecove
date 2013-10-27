from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','deviceapp.views.index'),
    url(r'^imageupload','deviceapp.views.imageupload'),
    url(r'^searchquery','deviceapp.views.searchquery'),
    url(r'^autosuggest','deviceapp.views.autosuggest'),
    url(r'^productpreview/(?P<itemid>\w+)','deviceapp.views.productpreview'),
    url(r'^productsearch/(?P<industryterm>\w+)/(?P<devicecategoryterm>\w+)','deviceapp.views.productsearch'),
    url(r'^search','deviceapp.views.search'),
    url(r'^login','deviceapp.views.loginview'),
    url(r'^signup','deviceapp.views.signup'),
    url(r'^addproduct','deviceapp.views.addproduct'),
    url(r'^forgotpassword','deviceapp.views.forgotpassword'),
    url(r'^lgnrequest','deviceapp.views.lgnrequest'),
    url(r'^logout','deviceapp.views.logout_view'),
    url(r'^saveditems','deviceapp.views.saveditems'),
    url(r'^profile','deviceapp.views.profile'),
    url(r'^settings','deviceapp.views.settings'),
    url(r'^listeditems','deviceapp.views.listeditems'),
    url(r'^accounthistory','deviceapp.views.accounthistory'),
    url(r'^newuserform','deviceapp.views.newuserform'),
    url(r'^product/(?P<productid>\d+)/details','deviceapp.views.productdetails'),
    url(r'^product/(?P<productid>\d+)/buyingoptions','deviceapp.views.buyingoptions'),
    url(r'^profsettings/(?P<field>\w+)','deviceapp.views.updateprofsettings'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
