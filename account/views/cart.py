from django.views import generic
from ..models import Cart




class CartView(generic.TemplateView):
    template_name = 'account/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['cart'] = self.request.user.carts.filter(paid=False).first()
        context['cart'] = Cart.objects.filter(paid=False).first()
        return context

