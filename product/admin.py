from django.contrib import admin
from .models import Category, Product, ProductImage
from utils import get_title, format_price



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'category', 'get_price', 'quantity', 'sales_count', 'has_cover', 'public')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'width: 50em;'
        form.base_fields['price'].widget.attrs['style'] = 'width: 12em;'
        form.base_fields['quantity'].widget.attrs['style'] = 'width: 12em;'
        form.base_fields['sales_count'].widget.attrs['style'] = 'width: 12em;'
        return form
    
    def product_title(self, obj):
        return get_title(obj.title)
    product_title.short_description = 'title'

    def get_price(self, obj):
        return format_price(obj.price, lang='en')
    get_price.short_description = 'price'

    def has_cover(self, obj):
        return bool(obj.cover)
    has_cover.boolean = True
    has_cover.short_description = 'cover'



admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)