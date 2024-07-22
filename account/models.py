from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator
from .manager import UserManager
from product.models import ProductSizeColor
from utils import get_title, format_price, get_types, validate_time, persian_date, persian_numbers_converter



class User(AbstractBaseUser):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True, editable=False)
    # favorite_products = models.ManyToManyField('product.Product', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return self.name or '-'
    
    def has_perm(self, perm, obj=None):
        return self.is_staff and self.is_superuser
    
    def has_module_perms(self, module):
        return self.is_staff and self.is_superuser



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product_size_color = models.ForeignKey(ProductSizeColor, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    paid = models.BooleanField(default=False)

    def __str__(self):
        return get_title(self.product_size_color.product.title, length=50)
    
    def total_price(self):
        return self.product_size_color.product.price_after_discount() * self.quantity
    
    def total_price_fa(self):
        return format_price(self.total_price(), lang='fa')
    
    def product_types(self):
        return get_types(self.product_size_color)
    
    def product_types_list(self):
        return get_types(self.product_size_color).split(' - ')



class Cart(models.Model):
    STATUSES = (
        ('unpaid', 'unpaid'),
        ('sending', 'sending'),
        ('delivered', 'delivered'),
        ('returned', 'returned'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='carts')
    orders = models.ManyToManyField(Order, blank=True)
    order_code = models.AutoField(primary_key=True, unique=True)
    order_description = models.TextField(null=True, blank=True)

    # Address
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    recipient_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Paying
    paid = models.BooleanField(default=False)
    pay_time = models.DateTimeField(null=True, blank=True)
    amount_paid = models.CharField(max_length=50, null=True, blank=True)

    # Status
    status = models.CharField(choices=STATUSES, max_length=10, default='unpaid')
    status_reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(order.total_price() for order in self.orders.filter(paid=False).select_related('product_size_color__product'))
    
    def total_price_fa(self):
        return format_price(self.total_price(), lang='fa')
    
    def amount_paid_fa(self):
        return format_price(self.amount_paid, lang='fa')
    
    def jalali_payed_time(self):
        return persian_date(self.pay_time) if self.pay_time else None
    
    def persian_order_code(self):
        return persian_numbers_converter(str(self.order_code))
    
    def order_images(self):
        images = []
        for order in self.orders.select_related('product_size_color__product').filter(paid=True):
            product = order.product_size_color.product
            images.append({
                'image': product.cover.url,
                'product_title': product.title
            })
        return images
    
    def empty_orders(self):
        return sum(order.quantity for order in self.orders.all()) == 0



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    amount = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)



class OTPCode(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=5)
    created = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return validate_time(self.created)



class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    text = models.TextField()

    class Meta:
        verbose_name_plural = 'contact us'

