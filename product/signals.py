import os
from .models import Category, Product, ProductImage
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete




# ==================================================== Category ====================================================
@receiver(post_delete, sender=Category)
def category_auto_delete_cover_on_delete(sender, instance, **kwargs):
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)


@receiver(pre_save, sender=Category)
def category_auto_delete_cover_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try:
        old_cover = Category.objects.get(pk=instance.pk).cover
    except Category.DoesNotExist:
        return False
    
    new_cover = instance.cover
    if old_cover and old_cover != new_cover:
        if os.path.isfile(old_cover.path):
            os.remove(old_cover.path)





# ==================================================== Product ====================================================
@receiver(post_delete, sender=Product)
def product_auto_delete_cover_on_delete(sender, instance, **kwargs):
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)


@receiver(pre_save, sender=Product)
def product_auto_delete_cover_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try:
        old_cover = Product.objects.get(pk=instance.pk).cover
    except Product.DoesNotExist:
        return False
    
    new_cover = instance.cover
    if old_cover and old_cover != new_cover:
        if os.path.isfile(old_cover.path):
            os.remove(old_cover.path)






# ================================================== Product Image ==================================================
@receiver(post_delete, sender=ProductImage)
def product_auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=ProductImage)
def product_auto_delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try:
        old_image = ProductImage.objects.get(pk=instance.pk).image
    except ProductImage.DoesNotExist:
        return False
    
    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)

