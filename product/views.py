import random
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views import generic
from .models import Product, ProductImage
from utils import filtering




class HomeView(generic.TemplateView):
    template_name = 'product/home.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['discounters'] = Product.objects.filter(discount__gt=0, public=True).order_by('-created_at')
        context['recent_products'] = Product.objects.filter(public=True).order_by('-created_at')[:8]
        return context



class ProductListView(generic.TemplateView):
    template_name = 'product/shop.html'

    def get_context_data(self):
        products = filtering(queryset=Product.objects.filter(public=True), request=self.request)
        prices = products.values_list('price', flat=True)

        context = {
            'products': products,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
        }
        return context



class ProductDetailView(generic.DetailView):
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, title=self.kwargs.get('product_title'))
    
    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=obj)
        suggestion_products = Product.objects.exclude(id=obj.id).filter(category=obj.category)
        context['suggestion_products'] = sorted(
            random.sample(list(suggestion_products), min(suggestion_products.count(), 8)), key=lambda x:x.created_at, reverse=True
        )
        return context



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


