from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django_resized import ResizedImageField
from utils import get_title, format_price
from ckeditor.fields import RichTextField




class Category(models.Model):
    title = models.CharField(max_length=100)
    cover = ResizedImageField(upload_to='category_cover', force_format='WEBP', quality=100, size=[800, 800])

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title
    
    def product_count_fa(self):
        return format_price(self.products.count(), lang='fa')


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    properties = models.TextField()
    description = RichTextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    cover = ResizedImageField(upload_to='product_cover', force_format='WEBP', quality=100, size=[800, 800])

    purchase_price = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    sales_count = models.PositiveIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])

    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return get_title(self.title)
    
    def get_properties(self):
        return self.properties.split('-')
    
    def quantity(self):
        return sum(obj.quantity for obj in self.size_color.all())
    
    def quantity_fa(self):
        return format_price(self.quantity(), lang='fa')
    
    def is_available(self):
        return ProductSizeColor.objects.filter(product=self, quantity__gt=0).exists()
    
    def format_price_fa(self):
        return format_price(self.price, lang='fa')
    
    def price_after_discount(self):
        return round(self.price * ((100-self.discount) / 100))
    
    def price_after_discount_fa(self):
        return format_price(self.price_after_discount(), lang='fa')
    

class ProductImage(models.Model):
    image = ResizedImageField(upload_to='product_images/%Y/%m/', force_format='WEBP', quality=100, size=[800, 800])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.product.title} - image'
    
    class Meta:
        ordering = ('product',)



class Color(models.Model):
    color = models.CharField(max_length=20, unique=True)
    color_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.color
    
    class Meta:
        ordering = ('color',)

class Size(models.Model):
    size = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.size
    
    class Meta:
        ordering = ('size',)




class ProductSizeColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='size_color')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def quantity_fa(self):
        return format_price(self.quantity, lang='fa')

    def __str__(self):
        return f'{self.product.title[:20]} - {self.size} - {self.color} - {self.quantity}'

    class Meta:
        ordering = ['product']
        unique_together = ['product', 'size', 'color']
    
    def clean(self):
        size_bool, color_bool = bool(self.size), bool(self.color)
        
        if (size_bool or color_bool) and self.quantity < 1:
            raise ValidationError({'quantity': 'Either enter a number greater than 0 or leave the above two fields blank'})

