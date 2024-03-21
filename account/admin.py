from django.contrib import admin
from .models import User
from utils import elapsed_time



class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user_name', 'time', 'is_staff')
    readonly_fields = ('phone_number', 'password')

    def user_name(self, obj):
        return obj.name or '-'
    user_name.short_description = 'name'

    def time(self, obj):
        return elapsed_time(obj.created_at)


admin.site.register(User, UserAdmin)