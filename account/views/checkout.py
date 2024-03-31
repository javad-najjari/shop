from django.views import generic
from utils import get_user_cart




class CheckoutView(generic.TemplateView):
    template_name = 'account/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_user_cart(self.request.user)
        return context

