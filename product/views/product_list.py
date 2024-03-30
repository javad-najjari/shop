from django.views import generic
from ..models import Product
from utils import filtering





class ProductListView(generic.ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by_param = 'size'
    paginate_by = 12

    def get_queryset(self):
        return filtering(queryset=Product.objects.filter(public=True), request=self.request)
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get(self.paginate_by_param) or self.paginate_by

