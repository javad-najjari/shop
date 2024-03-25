import random
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import Product, ProductImage




class HomeView(generic.TemplateView):
    template_name = 'product/home.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['discounters'] = Product.objects.filter(discount__gt=0).order_by('-created_at')
        context['recent_products'] = Product.objects.order_by('-created_at')[:8]
        return context



class ProductListView(generic.TemplateView):
    template_name = 'product/shop.html'

    def get_context_data(self):
        products = Product.objects.filter(public=True)

        context = {
            'products': products,
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

