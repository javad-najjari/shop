from .models import Cart
from utils import format_price



def cart_detail(request):
    # orders_quantity = self.request.user.carts.filter(paid=False).first()
    orders_quantity = Cart.objects.filter(paid=False).first().orders.values_list('quantity', flat=True)

    return {
        'cart_products_count': format_price(sum(orders_quantity), lang='fa'),
    }

