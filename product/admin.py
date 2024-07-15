from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Size, Color, ProductSizeColor
from utils import get_title, format_price




class ProductImageInline(admin.StackedInline):
    model = ProductImage
    min_num = 3
    extra = 0
    verbose_name_plural = 'Images'

class ProductSizeColorInline(admin.StackedInline):
    model = ProductSizeColor
    min_num = 1
    extra = 0
    verbose_name = 'size color'
    verbose_name_plural = 'size color'


class ProductAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'product_title', 'get_cover', 'category', 'get_purchase_price', 'get_price', 'after_discount', 'profit',
        'sales_count', 'get_discount', 'kinds', 'public'
    )
    inlines = [ProductSizeColorInline, ProductImageInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'width: 50em;'
        form.base_fields['purchase_price'].widget.attrs['style'] = 'width: 12em;'
        form.base_fields['price'].widget.attrs['style'] = 'width: 12em;'
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
        return format_html('<span style="color:rgb(122, 122, 236);">{}</span>', price)
    get_price.short_description = 'price'

    def after_discount(self, obj):
        if obj.discount != 0:
            price = format_price(obj.price_after_discount())
        else:
            price = '-'
        return format_html('<span style="color:rgb(216, 86, 86);">{}</span>', price)
    
    def profit(self, obj):
        profit_display = format_price(obj.price_after_discount() - obj.purchase_price)
        return format_html('<span style="color:yellow;">{}</span>', profit_display)

    def get_discount(self, obj):
        discount = obj.discount
        if discount:
            return f'{discount}%'
        return '---'
    get_discount.short_description = 'discount'

    def kinds(self, obj):
        return obj.size_color.count() or None



class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'get_image')

    def product_title(self, obj):
        return get_title(obj.product.title, length=50)
    
    def get_image(self, obj):
        return format_html('<img src="{}" style="max-height:30px;" loading="lazy"/>'.format(obj.image.url))



class ProductSizeColorAdmin(admin.ModelAdmin):
    list_display = ('get_product', 'size', 'color', 'quantity')

    def get_product(self, obj):
        return get_title(obj.product.title, length=50)



class ColorAdmin(admin.ModelAdmin):
    list_display = ('color', 'color_code')



admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Size)
admin.site.register(Color, ColorAdmin)
admin.site.register(ProductSizeColor, ProductSizeColorAdmin)