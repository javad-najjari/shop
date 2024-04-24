from utils import format_price, get_user_cart



def cart_detail(request):
    
    if request.user.is_authenticated:
        orders = get_user_cart(request.user).orders.all()
        if orders:
            orders_quantity = orders.values_list('quantity', flat=True)

            return {
                'cart_products_count': format_price(sum(orders_quantity), lang='fa'),
            }
    
    return {}

