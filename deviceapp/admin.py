from django.contrib import admin
from deviceapp.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.register(Industry)
admin.site.register(DeviceCategory)
admin.site.register(Product)
admin.site.register(Item)
admin.site.register(UserImage)
admin.site.register(TestImage)
# class BasicUserInline(admin.StackedInline):
# 	model = BasicUser
# 
# class UserAdmin(UserAdmin):
#     inlines = (BasicUserInline,)
#     
# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)


admin.site.register(BasicUser)
