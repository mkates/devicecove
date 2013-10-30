from django.contrib import admin
from deviceapp.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'displayname'] 
admin.site.register(Industry, IndustryAdmin)

admin.site.register(DeviceCategory)
admin.site.register(SavedItem)
admin.site.register(Product)
admin.site.register(Item)
admin.site.register(UserImage)
admin.site.register(BasicUser)
