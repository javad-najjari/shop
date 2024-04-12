from django.urls import path
from . import views



app_name = 'account'

urlpatterns = [
    # cart
    path('account/cart/', views.CartView.as_view(), name='cart'),
    path('quantity-in-cart/', views.QuantityInCartView.as_view(), name='quantity-in-cart'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('account/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),

    # authentication
    path('account/login/', views.UserLoginView.as_view(), name='login'),

    # profile
    path('profile/orders', views.OrderHistoryView.as_view(), name='orders'),

    path('payment/', views.PaymentPageView.as_view(), name='payment'),
    path('payment-verify/', views.PaymentVerifyView.as_view(), name='payment-verify'),
    
]
