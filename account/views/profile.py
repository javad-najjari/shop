from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin




class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/profile.html'

