from django.shortcuts import get_list_or_404
from django.views import generic
from ..models import Product
from utils import filtering




class SearchView(generic.ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        title = self.request.GET.get('title')
        products = filtering(queryset=Product.objects.filter(title__icontains=title), request=self.request)
        return get_list_or_404(products)
    
    def get_context_data(self):
        context = super().get_context_data()
        prices = [product.price for product in self.get_queryset()]
        
        context['min_price'] = min(prices)
        context['max_price'] = max(prices)

        return context

