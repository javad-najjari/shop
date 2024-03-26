from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage
from utils import get_title, format_price




class ProductImageInline(admin.StackedInline):
    model = ProductImage
    min_num = 3
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_title', 'get_cover', 'category', 'get_purchase_price', 'get_price', 'after_discount', 'profit', 'quantity',
        'sales_count', 'get_discount', 'has_cover', 'public'
    )
    inlines = [ProductImageInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'width: 50em;'
        form.base_fields['purchase_price'].widget.attrs['style'] = 'width: 12em;'
        form.base_fields['price'].widget.attrs['style'] = 'width: 12em;'
        form.base_fields['quantity'].widget.attrs['style'] = 'width: 12em;'
        form.base_fields['sales_count'].widget.attrs['style'] = 'width: 12em;'
        form.base_fields['discount'].widget.attrs['style'] = 'width: 12em;'
        return form
    
    def product_title(self, obj):
        return get_title(obj.title, length=20)
    product_title.short_description = 'title'

    def get_cover(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="max-height:30px;" loading="lazy"/>'.format(obj.cover.url))
    get_cover.short_description = 'cover'

    def get_purchase_price(self, obj):
        price = format_price(obj.purchase_price)
        return format_html('<span style="color:green;">{}</span>', price)
    get_purchase_price.short_description = 'purchase price'

    def get_price(self, obj):
        price = format_price(obj.price, lang='en')
        return format_html('<span style="color:blue;">{}</span>', price)
    get_price.short_description = 'price'

    def after_discount(self, obj):
        if obj.discount != 0:
            price = format_price(obj.price_after_discount())
        else:
            price = '-'
        return format_html('<span style="color:red;">{}</span>', price)
    
    def profit(self, obj):
        profit_display = format_price(obj.price_after_discount() - obj.purchase_price)
        return format_html('<span style="color:yellow;">{}</span>', profit_display)

    def get_discount(self, obj):
        discount = obj.discount
        if discount:
            return f'{discount}%'
        return '---'
    get_discount.short_description = 'discount'

    def has_cover(self, obj):
        return bool(obj.cover)
    has_cover.boolean = True
    has_cover.short_description = 'cover'



class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'get_image')

    def product_title(self, obj):
        return get_title(obj.product.title, length=50)
    
    def get_image(self, obj):
        return format_html('<img src="{}" style="max-height:30px;" loading="lazy"/>'.format(obj.image.url))



admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)