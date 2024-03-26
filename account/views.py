from django.views import generic




class CartView(generic.TemplateView):
    template_name = 'account/cart.html'



class ContactUsView(generic.TemplateView):
    template_name = 'account/contact-us.html'

