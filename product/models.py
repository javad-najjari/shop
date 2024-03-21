from django.db import models
from utils import get_title, format_price




class Category(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='category_cover')

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='product_cover')

    price = models.PositiveIntegerField()
    quantity = models.SmallIntegerField()
    sales_count = models.PositiveIntegerField(default=0)

    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return get_title(self.title)
    
    def format_price_fa(self):
        return format_price(self.price, lang='fa')
    

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/%Y/%m/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.product.title} - image'

