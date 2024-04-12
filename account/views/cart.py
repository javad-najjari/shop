from django.views.generic import TemplateView
from utils import get_user_cart, get_user_orders
from django.contrib.auth.mixins import LoginRequiredMixin




class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'account/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_user_cart(self.request.user)
        orders = get_user_orders(user=self.request.user)
        context['cart'] = cart
        context['orders'] = orders.filter(quantity__gt=0).order_by('product_size_color__product__title')
        return context

