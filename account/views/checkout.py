from django.views import generic
from utils import get_user_cart




class CheckoutView(generic.TemplateView):
    template_name = 'account/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_user_cart(self.request.user)
        context['cart'] = cart
        context['orders'] = cart.orders.filter(quantity__gt=0).order_by('product_size_color__product__title')
        return context

