from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Order, Cart, Payment, OTPCode, ContactUs
from utils import elapsed_time, get_title



class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user_name', 'time', 'is_staff')
    readonly_fields = ('phone_number', 'password')

    def user_name(self, obj):
        return obj.name or '-'
    user_name.short_description = 'name'

    def time(self, obj):
        return elapsed_time(obj.created_at)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_size_color', 'quantity', 'paid')



class CartAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'user', 'orders_count', 'paid', 'status')

    def orders_count(self, obj):
        return sum(order.quantity for order in obj.orders.all())



class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'is_valid')

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True



class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'get_text')

    def get_text(self, obj):
        return get_title(obj.text)
    get_text.short_descripton = 'text'




admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Payment)
admin.site.register(OTPCode, OTPCodeAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.unregister(Group)