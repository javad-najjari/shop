from django.views import generic
from ..models import Product
from utils import product_filtering





class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by_param = 'size'
    paginate_by = 12

    def get_queryset(self):
        return product_filtering(queryset=Product.objects.filter(public=True), request=self.request)
    
    def get_paginate_by(self, queryset):
        paginate_param = self.request.GET.get(self.paginate_by_param, None)

        return paginate_param if paginate_param in ['9', '12', '15'] else self.paginate_by

