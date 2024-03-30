from django.views import generic




class ContactUsView(generic.TemplateView):
    template_name = 'account/contact-us.html'

