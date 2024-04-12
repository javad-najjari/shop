from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from utils import get_user_cart, more_than_stock, get_user_orders
from ..models import Order, ProductSizeColor




class AddToCartView(View):

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'status': 401})

        type_id = request.POST.get('selected_type')
        button = request.POST.get('button')

        product_size_color = get_object_or_404(ProductSizeColor, id=type_id)
        cart = get_user_cart(user)
        orders = get_user_orders(user=user)

        order = orders.filter(product_size_color=product_size_color, user=user, paid=False).last()
        if not order:
            order = Order.objects.create(user=user, product_size_color=product_size_color, quantity=0)
            cart.orders.add(order)
            cart.save()

        quantity = order.quantity

        if button == 'add':
            if more_than_stock(product_size_color, quantity):
                # return JsonResponse({'error': 'تعداد درخواستی بیشتر از موجودی است.'}, status=400)
                return JsonResponse({})
            order.quantity += 1
            order.save()

        elif button == 'minus' and quantity > 0:
            order.quantity -= 1
            order.save()
        
        return JsonResponse({
            
        })

