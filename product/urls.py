from django.urls import path
from . import views



app_name = 'product'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/', views.ProductListView.as_view(), name='list'),
    path('product/<str:product_title>/', views.ProductDetailView.as_view(), name='detail'),
]