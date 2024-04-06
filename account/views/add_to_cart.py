from django.views.generic import View
from django.http import JsonResponse
from utils import get_user_cart, get_quantity_in_cart




class AddToCartView(View):

    def post(self, request):
        type_id = request.POST.get('selected_type')
        count_in_cart = get_quantity_in_cart(product_size_color_id=type_id, user=request.user)

        return JsonResponse({
            'count_in_cart': count_in_cart,
        })

