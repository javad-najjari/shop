from django.views import generic
from utils import get_user_cart




class CartView(generic.TemplateView):
    template_name = 'account/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_user_cart(self.request.user)
        context['cart'] = cart
        context['orders'] = cart.orders.order_by('product_size_color__product__title')
        return context

