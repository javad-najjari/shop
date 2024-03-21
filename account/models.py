from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager



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

