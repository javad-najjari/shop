from django.views import generic
from ..models import Product, Category, ProductImage



class HomeView(generic.TemplateView):
    template_name = 'product/shop.html'

    def get_context_data(self):
        products = Product.objects.filter(public=True)

        context = {
            'products': products,
        }
        return context

