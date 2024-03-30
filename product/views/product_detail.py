import random
from django.shortcuts import get_object_or_404
from django.views import generic
from ..models import Product, ProductImage
from utils import get_types




class ProductDetailView(generic.DetailView):
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, title=self.kwargs.get('product_title'), public=True)
    
    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=obj)
        product_size_colors = obj.size_color.select_related('size', 'color')
        # if product_size_colors:
        #     sizes = list(set(p.size for p in product_size_colors))
        #     colors = list(set(p.color for p in product_size_colors))

        #     context['sizes'] = sizes if not all(item is None for item in sizes) else None
        #     context['colors'] = colors if not all(item is None for item in colors) else None

        if product_size_colors:
            context['types'] = [
                {'text': get_types(obj), 'size': obj.size, 'color': obj.color} for obj in product_size_colors
            ]

        suggestion_products = Product.objects.exclude(id=obj.id).filter(category=obj.category, public=True)
        context['suggestion_products'] = sorted(
            random.sample(list(suggestion_products), min(suggestion_products.count(), 8)), key=lambda x:x.created_at, reverse=True
        )
        return context

