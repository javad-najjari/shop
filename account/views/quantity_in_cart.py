from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from utils import get_user_cart, get_quantity_in_cart, more_than_stock
from ..models import ProductSizeColor




class QuantityInCartView(View):

    def post(self, request):
        type_id = request.POST.get('selected_type')
        
        if type_id:
            count_in_cart = get_quantity_in_cart(product_size_color_id=type_id, user=request.user)
            limited_stock = more_than_stock(get_object_or_404(ProductSizeColor, id=type_id), count=count_in_cart)

            return JsonResponse({
                'count_in_cart': count_in_cart,
                'limited_stock': limited_stock,
            })
        
