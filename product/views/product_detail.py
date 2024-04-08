import random
from django.shortcuts import get_object_or_404
from django.views import generic
from ..models import Product, ProductImage
from utils import get_types, get_user_cart, get_quantity_in_cart, custom_sort_key




class ProductDetailView(generic.DetailView):
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, title=self.kwargs.get('product_title'), public=True)
    
    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)

        context['images'] = ProductImage.objects.filter(product=obj)
        context['cart'] = get_user_cart(self.request.user)
        
        product_size_colors = list(obj.size_color.select_related('size', 'color'))
        type_id = self.request.GET.get('type_id')
        if type_id:
            product_size_colors = sorted(product_size_colors, key=custom_sort_key(type_id))

        if len(product_size_colors) > 1:
            context['types'] = [
                {'id': obj.id, 'text': get_types(obj), 'size': obj.size, 'color': obj.color,} for obj in product_size_colors
            ]
        
        suggestion_products = Product.objects.exclude(id=obj.id).filter(category=obj.category, public=True)
        context['suggestion_products'] = sorted(
            random.sample(list(suggestion_products), min(suggestion_products.count(), 8)), key=lambda x:x.created_at, reverse=True
        )

        product_size_color_id = product_size_colors[0].id if product_size_colors else None

        if product_size_color_id:
            context['count_in_cart'] = get_quantity_in_cart(product_size_color_id=product_size_color_id, user=self.request.user)

        return context

