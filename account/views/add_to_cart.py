from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import get_user_cart, more_than_stock
from ..models import Order, ProductSizeColor


from django.db import connection




class AddToCartView(View):

    def post(self, request):

        type_id = request.POST.get('selected_type')
        button = request.POST.get('button')

        print(f'{"="*50} Start => {len(connection.queries)} queries {"="*50}')

        cart = get_user_cart(request.user)
        product_size_color = get_object_or_404(ProductSizeColor, id=type_id)
        order = cart.orders.filter(product_size_color=product_size_color).first()

        quantity = order.quantity if order else None

        if button == 'add':
            if quantity and more_than_stock(product_size_color, quantity):
                # return JsonResponse({'error': 'تعداد درخواستی بیشتر از موجودی است.'}, status=400)
                return JsonResponse({})

            if order:
                new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=quantity+1)[0]
                cart.orders.add(new_order)
                cart.orders.remove(order)
                cart.save()
            else:
                new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=1)[0]
                cart.orders.add(new_order)
                cart.save()
        elif button == 'minus' and quantity > 0:
            if order:
                if quantity != 1:
                    new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=quantity-1)[0]
                    cart.orders.add(new_order)
                cart.orders.remove(order)
                cart.save()
            else:
                new_order = Order.objects.get_or_create(product_size_color=product_size_color, quantity=1)[0]
                cart.orders.add(new_order)
                cart.save()
        
        print(f'{"="*50} End => {len(connection.queries)} queries {"="*50}')

        return JsonResponse({
            
        })

