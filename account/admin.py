from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Order, Cart, UserAddress, Payment, OTPCode
from utils import elapsed_time



class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user_name', 'time', 'is_staff')
    readonly_fields = ('phone_number', 'password')

    def user_name(self, obj):
        return obj.name or '-'
    user_name.short_description = 'name'

    def time(self, obj):
        return elapsed_time(obj.created_at)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_size_color', 'quantity')



class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'is_valid')

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True



admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(UserAddress)
admin.site.register(Payment)
admin.site.register(OTPCode, OTPCodeAdmin)
admin.site.unregister(Group)