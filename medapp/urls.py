from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','deviceapp.views.index'),
    url(r'^search','deviceapp.views.search'),
    url(r'^login','deviceapp.views.loginview'),
    url(r'^signup','deviceapp.views.signup'),
    url(r'^addproduct','deviceapp.views.addproduct'),
    url(r'^forgotpassword','deviceapp.views.forgotpassword'),
    url(r'^product','deviceapp.views.product'),
    url(r'^lgnrequest','deviceapp.views.lgnrequest'),
    url(r'^logout','deviceapp.views.logout_view'),
    url(r'^saveditems','deviceapp.views.saveditems'),
    url(r'^profile','deviceapp.views.profile'),
    url(r'^settings','deviceapp.views.settings'),
    url(r'^listeditems','deviceapp.views.listeditems'),
    url(r'^accounthistory','deviceapp.views.accounthistory'),
    url(r'^newuserform','deviceapp.views.newuserform'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
