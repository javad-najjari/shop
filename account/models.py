from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator
from .manager import UserManager
from product.models import ProductSizeColor
from utils import get_title, format_price, get_types



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



class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
    address = models.TextField()
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    recipient_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True)
    
    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'user addresses'
    
    def __str__(self):
        return self.address



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product_size_color = models.ForeignKey(ProductSizeColor, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return get_title(self.product_size_color.product.title, length=50)

    class Meta:
        unique_together = ['product_size_color', 'quantity']
    
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
        ('delivered', 'delivered'),
        ('returned', 'returned'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='carts')
    orders = models.ManyToManyField(Order, blank=True)
    order_code = models.AutoField(primary_key=True, unique=True)
    order_description = models.TextField(null=True, blank=True)

    # Address
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    address_text = models.TextField(blank=True)
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
        return sum(order.total_price() for order in self.orders.all())
    
    def total_price_fa(self):
        return format_price(self.total_price(), lang='fa')



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_code = models.CharField(max_length=10)
    amount = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

