from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import get_user_cart, more_than_stock
from ..models import Order, ProductSizeColor


from django.db import connection




class AddToCartView(View):

    def post(self, request):
        # TODO: 2 lines below must change
        from ..models import User
        user = User.objects.first()

        type_id = request.POST.get('selected_type')
        button = request.POST.get('button')

        print(f'{"="*30} {len(connection.queries)}', end=' => ')

        product_size_color = get_object_or_404(ProductSizeColor, id=type_id)
        cart = get_user_cart(user)
        orders = cart.orders.all()

        order = orders.filter(product_size_color=product_size_color, user=user).last()
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
        
        print(f'{len(connection.queries)} {"="*30}')

        return JsonResponse({
            
        })

