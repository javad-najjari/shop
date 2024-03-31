import json
import requests
from decouple import config
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Cart, Payment



User = get_user_model()



ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"


class PaymentPageView(LoginRequiredMixin, View):

    def get(self, request):
        messages.success(request, 'پرداخت موفق - سفارش شما به زودی ارسال میشود')
        return redirect('account:cart')
        
        # cart = get_object_or_404(Cart, user=request.user, paid=False)

        # if cart.orders.count() == 0:
        #     return Response({'detail': no_order(request)}, status=404)
        
        # for order in cart.orders.all().select_related('product_color'):
        #     if order.product_color.stock < order.count:
        #         return Response({'detail': more_than_stock_2(order.product_color.product, lang)}, status=400)

        # amount = cart_final_price(cart, lang='fa')
        # data = {
        #     "MerchantID": config('MERCHANT'),
        #     "Amount": amount,
        #     "Description": f'پرداخت محصولات به مبلغ کل {amount} تومان',
        #     "Phone": cart.user.phone_number,
        #     "CallbackURL": f'{config("CALLBACKURL", None)}?order_code={cart.order_code}&user={request.user.id}',
        # }
        
        # data = json.dumps(data)
        # headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        
        # try:
        #     response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        #     if response.status_code == 200:
        #         response = response.json()
        #         if response['Status'] == 100:
        #             return Response({
        #                 'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']
        #             })
        #         else:
        #             return Response({'status': False, 'code': str(response['Status'])})
        #     return Response(response)
        
        # except requests.exceptions.Timeout:
        #     return Response({'status': False, 'code': 'timeout'})
        # except requests.exceptions.ConnectionError:
        #     return Response({'status': False, 'code': 'connection error'})



class PaymentVerifyView(View):

    def get(self, request):
        user = get_object_or_404(User, id=request.GET.get('user', None))
        request.user = user
        authority = request.GET.get('Authority')
        cart = get_object_or_404(Cart, user=request.user, paid=False)
        amount = cart_final_price(cart, lang='fa')

        data = {
            "MerchantID": config('MERCHANT'),
            "Amount": amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()

            if response['Status'] == 100:
                after_payment(cart, request)
                Payment.objects.create(
                    user = request.user,
                    order_code = cart.order_code,
                    amount = amount,
                    ref_id = response['RefID'],
                )
                return redirect('https://yalfan.com/profile/orders')
            else:
                return redirect(config('CALLBACKURLFAIL', None))
        return redirect(config('CALLBACKURLFAIL', None))

