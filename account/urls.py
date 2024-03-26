from django.urls import path
from . import views



app_name = 'account'

urlpatterns = [
    path('account/cart/', views.CartView.as_view(), name='cart'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),
]