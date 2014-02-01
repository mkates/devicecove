from django.contrib import admin
from deviceapp.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'displayname'] 
admin.site.register(Industry, IndustryAdmin)

class ItemAdmin(admin.ModelAdmin):
	list_display = ['id','user','name','price','liststatus','creation_date','savedcount','subcategory','manufacturer','serialno','modelyear','originalowner','contract','conditiontype','conditionquality','shippingincluded']
admin.site.register(Item, ItemAdmin)

admin.site.register(Category)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(SavedItem)
admin.site.register(BasicUser)
admin.site.register(Question)
