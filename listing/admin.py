from django.contrib import admin
from listing.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'displayname'] 
admin.site.register(Industry)

admin.site.register(Item)
admin.site.register(Equipment)
admin.site.register(NewEquipment)
admin.site.register(UsedEquipment)
admin.site.register(PharmaBase)
admin.site.register(PharmaItem)