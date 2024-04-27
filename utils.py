from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from jalali_date import datetime2jalali




def persian_numbers_converter(mystr):
    jnumbers = {
        '0' : '۰',
        '1' : '۱',
        '2' : '۲',
        '3' : '۳',
        '4' : '۴',
        '5' : '۵',
        '6' : '۶',
        '7' : '۷',
        '8' : '۸',
        '9' : '۹',
    }

    for e, p in jnumbers.items():
        mystr = mystr.replace(e, p)
    return mystr


def english_numbers_converter(mystr):
    if not mystr:
        return None

    pnumbers = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
    }

    for p, e in pnumbers.items():
        mystr = mystr.replace(p, e)
    return mystr


def elapsed_time(created):
    time = (timezone.now() - created).total_seconds()

    if time < 1:
        return 'right_now'
    elif time < 60:
        return f'{int(time)} seconds ago'
    elif time < 3600:
        if time // 60 == 1:
            return '1 minute ago'
        return f'{int(time//60)} minutes ago'
    elif time < 86400:
        if time // 3600 == 1:
            return '1 hour ago'
        return f'{int(time // 3600)} hours ago'
    elif time < 604800:
        if time // 86400 == 1:
            return '1 day ago'
        return f'{int(time // 86400)} days ago'
    elif time // 604800 == 1:
        return '1 week ago'
    return f'{int(time // 604800)} weeks ago'


def get_title(title, length=None):
    length = length or 30
    return title if len(title) < length else title[:length] + ' ...'


def format_price(number, lang='en'):
    if number is None:
        return 0

    reversed_number = str(number)[::-1]
    formatted_parts = []

    for i in range(0, len(reversed_number), 3):
        part = reversed_number[i:i + 3]
        formatted_parts.append(part)

    if lang == 'en':
        return ",".join(formatted_parts)[::-1]
    
    return persian_numbers_converter(",".join(formatted_parts)[::-1])


def ordering_by_existing_products(queryset):
    from product.models import ProductSizeColor
    queryset_ids = ProductSizeColor.objects.filter(product__in=[q.id for q in queryset], quantity__gt=0).values_list('product', flat=True)
    return sorted(queryset, key=lambda x:x.id in queryset_ids, reverse=True)


def product_filtering(queryset, request):
    category, search = request.GET.get('category'), request.GET.get('search')
    sort = request.GET.get('sort')

    if category:
        queryset = queryset.filter(category__title=category)
    
    if search:
        queryset = queryset.filter(title__icontains=search)
    
    if sort:
        sort_keys = {
            '1': 'price',
            '2': '-price',
            '3': '-created_at',
            '4': 'created_at',
            '5': 'exist',
            '6': '-sales_count'
        }
        if sort == '5':
            queryset = ordering_by_existing_products(queryset)
        elif sort in sort_keys:
            queryset = queryset.order_by(sort_keys[sort])
    
    return queryset


def get_types(obj):
    size, color = obj.size, obj.color
    if size and color:
        return f'{obj.color} - سایز {obj.size}'
    elif size:
        return f'سایز {obj.size}'
    elif color:
        return f'{obj.color}'
    return '-'


def get_user_cart(user):
    from account.models import Cart

    if user.is_authenticated:
        return Cart.objects.get_or_create(user=user, paid=False)[0]
    
    return None


def get_quantity_in_cart(product_size_color_id, user):
    cart = get_user_cart(user)
    orders = cart.orders.all() if cart else None

    if orders:
        order = orders.filter(product_size_color__id=product_size_color_id)
        if order.exists():
            return order.first().quantity
    
    return 0


def more_than_stock(product_size_color, count):
    return (count + 1) > product_size_color.quantity


def custom_sort_key(type_id):
    def inner_sort_key(item):
        if type_id.isdigit() and item.id == int(type_id):
            return (0,)
        else:
            return (1, item.id)

    return inner_sort_key


def validate_time(created):
    elapsed_time = timezone.now() - created
    valid_seconds = settings.SMS_VALIDITY_SECONDS
    return elapsed_time.seconds < valid_seconds


def is_valid_phone_number(phone_number):

    if not (phone_number is not None and phone_number.startswith('09') and phone_number.isdigit() and len(phone_number) == 11):
        return False
    
    return True


def permission_to_send_sms(phone_number):
    from account.models import OTPCode

    codes = OTPCode.objects.filter(phone=phone_number)
    if not codes.exists():
        return True
    return not any(code.is_valid() for code in codes)


def get_next_url(request):
    if 'next_url' in request.session:
        return request.session['next_url']
    else:
        return reverse('product:home')


def gregorian_to_jalali(date):
    jalali_date = datetime2jalali(date)
    return f'{jalali_date.year}/{jalali_date.month}/{jalali_date.day}'


def persian_date(date):
    j_date = gregorian_to_jalali(date)
    year, month, day = j_date.split('/')
    year, day = persian_numbers_converter(year), persian_numbers_converter(day)
    
    j_months = {
        '1': 'فروردین',
        '2': 'اردیبهشت',
        '3': 'خرداد',
        '4': 'تیر',
        '5': 'مرداد',
        '6': 'شهریور',
        '7': 'مهر',
        '8': 'آبان',
        '9': 'آذر',
        '10': 'دی',
        '11': 'بهمن',
        '12': 'اسفند',
    }
    
    return f'{day} {j_months[month]} {year}'


def get_user_address_information(user, current_cart, previous_cart):
    

        if current_cart and current_cart.recipient_name:
            return {
                'recipient_name': current_cart.recipient_name,
                'phone_number': current_cart.phone_number,
                'address': current_cart.address,
                'postal_code': current_cart.postal_code,
            }
        elif previous_cart:
            return {
                'recipient_name': previous_cart.recipient_name,
                'phone_number': previous_cart.phone_number,
                'address': previous_cart.address,
                'postal_code': previous_cart.postal_code,
            }
        else:
            return {
                'recipient_name': user.name,
                'phone_number': user.phone_number,
            }


def clean_cart(cart):
    # TODO: اردرهایی که توی سبد خرید نیستن کلا باید پاک بشن
    orders = cart.orders.filter(quantity=0)

    if orders.exists():
        for order in orders:
            cart.orders.remove(order)
        cart.save()


def out_of_stock(cart, request):
    for order in cart.orders.select_related('product_size_color'):
        if order.product_size_color.quantity < order.quantity:
            cart.orders.remove(order)
            cart.save()
            messages.error(request, f'موجودی محصول {get_title(order.product_size_color.product.title, length=10)} تمام شده است و از سبد خرید شما حذف شد')
            return True
    return False


def after_payment(cart, amount):
    orders = cart.orders.filter(quantity__gt=0).select_related('product_size_color__product')
    for order in orders:
        psc = order.product_size_color
        psc.quantity -= order.quantity
        psc.product.sales_count += order.quantity
        psc.save()
        psc.product.save()

    cart.paid = True
    cart.pay_time = timezone.now()
    cart.status = 'sending'
    cart.amount_paid = amount
    cart.save()

