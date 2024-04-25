from django.views import generic
from ..models import Product
from utils import ordering_by_existing_products




class HomeView(generic.TemplateView):
    template_name = 'product/home.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['discounters'] = ordering_by_existing_products(Product.objects.filter(discount__gt=0, public=True))
        context['recent_products'] = Product.objects.filter(public=True).order_by('-created_at')[:8]
        return context

