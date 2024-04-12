from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin




class OrderHistoryView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/order_history.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context['paid_carts'] = user.carts.filter(paid=True).order_by('-pay_time')

        return context

