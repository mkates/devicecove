from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','deviceapp.views.index'),
    url(r'^search','deviceapp.views.search'),
    url(r'^login','deviceapp.views.login'),
    url(r'^signup','deviceapp.views.signup'),
    url(r'^addproduct','deviceapp.views.addproduct'),
    url(r'^forgotpassword','deviceapp.views.forgotpassword'),
    url(r'^product','deviceapp.views.product'),
     
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
