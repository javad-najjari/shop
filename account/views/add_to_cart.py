from django.views.generic import View
from django.http import JsonResponse
from utils import get_user_cart, get_quantity_in_cart
from ..models import Order, ProductSizeColor




class AddToCartView(View):

    def post(self, request):

        type_id = request.POST.get('selected_type')
        button = request.POST.get('button')
        count_in_cart = get_quantity_in_cart(product_size_color_id=type_id, user=request.user)

        cart = get_user_cart(request.user)
        orders = cart.orders.all()
        order = orders.filter(product_size_color__id=type_id).first()
        product_size_color = ProductSizeColor.objects.get(id=type_id)

        if button == 'add':
            if order:
                new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=order.quantity+1)[0]
                cart.orders.remove(order)
                cart.orders.add(new_order)
                cart.save()
            else:
                new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=1)[0]
                cart.orders.add(new_order)
                cart.save()
        elif button == 'minus' and order.quantity > 0:
            if order:
                new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=order.quantity-1)[0]
                cart.orders.remove(order)
                cart.orders.add(new_order)
                cart.save()
            else:
                new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=1)[0]
                cart.orders.add(new_order)
                cart.save()


        return JsonResponse({
            'count_in_cart': count_in_cart
        })

