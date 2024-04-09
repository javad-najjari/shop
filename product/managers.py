from django.db import models
from django.db.models import Exists, OuterRef
from .models import ProductSizeColor



class ProductManager(models.Manager):
    def get_queryset(self):
        # ایجاد یک subquery برای تشخیص موجودیت محصول
        product_size_color_subquery = ProductSizeColor.objects.filter(
            product=OuterRef('pk'), 
            quantity__gt=0
        )
        
        return super().get_queryset().annotate(
            is_available=Exists(product_size_color_subquery)
        ).order_by('-is_available', 'title')

