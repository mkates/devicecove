from django.contrib import admin
from deviceapp.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'displayname'] 
admin.site.register(Industry, IndustryAdmin)

class ItemAdmin(admin.ModelAdmin):
	list_display = ['id','user','product','devicecategory','age','type','contract','liststatus','price','savedcount']
admin.site.register(Item, ItemAdmin)

class ItemImageAdmin(admin.ModelAdmin):
	list_display = ['id','item','photo']
admin.site.register(ItemImage, ItemImageAdmin)

class ProductImageAdmin(admin.ModelAdmin):
	list_display = ['id','photo']
admin.site.register(ProductImage, ProductImageAdmin)

admin.site.register(DeviceCategory)
admin.site.register(SavedItem)
admin.site.register(BasicUser)
