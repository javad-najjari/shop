from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views



app_name = 'account'

urlpatterns = [
    # cart
    path('account/cart/', views.CartView.as_view(), name='cart'),
    path('account/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('quantity-in-cart/', views.QuantityInCartView.as_view(), name='quantity-in-cart'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),

    # authentication
    path('account/login/', views.UserLoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/orders', views.OrderHistoryView.as_view(), name='orders'),

    # contact us
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),

    # payment
    path('payment/', views.PaymentPageView.as_view(), name='payment'),
    path('payment-verify/', views.PaymentVerifyView.as_view(), name='payment-verify'),
    
]
