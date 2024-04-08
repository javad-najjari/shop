from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import get_user_cart, more_than_stock, action_buttons
from ..models import Order, ProductSizeColor




class AddToCartView(View):

    def post(self, request):

        type_id = request.POST.get('selected_type')
        product_id = request.POST.get('product_id')

        button = request.POST.get('button')
        cart = get_user_cart(request.user)

        if type_id:
            order = cart.orders.filter(product_size_color__id=type_id).first()
            product_size_color = get_object_or_404(ProductSizeColor, id=type_id)
            quantity = order.quantity if order else None
            
            action_buttons(
                button=button,
                quantity = quantity,
                product_size_color = product_size_color,
                order = order,
                cart = cart,
            )
        elif product_id:
            product_size_color = ProductSizeColor.objects.filter(product__id=product_id).first()
            if product_size_color in cart.orders.all():
                order = cart.orders.filter(product_size_color=product_size_color).first()
            else:
                order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=1)[0]

        return JsonResponse({
            
        })

