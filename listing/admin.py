from django.contrib import admin
from listing.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'displayname'] 
admin.site.register(Industry)

admin.site.register(Product)
admin.site.register(Item)
