from django.views import generic
from ..models import Product, Category, ProductImage




class HomeView(generic.TemplateView):
    template_name = 'product/home.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['discounters'] = Product.objects.filter(discount__gt=0)
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

