from django.urls import path
from . import views



app_name = 'account'

urlpatterns = [
    path('account/cart/', views.CartView.as_view(), name='cart'),
    path('account/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),

    path('payment/', views.PaymentPageView.as_view(), name='payment'),
    path('payment-verify/', views.PaymentVerifyView.as_view(), name='payment-verify'),
]
