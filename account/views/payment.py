import json
import requests
from decouple import config
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Cart, Payment
from utils import clean_cart, out_of_stock, after_payment



User = get_user_model()



ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"


class PaymentPageView(LoginRequiredMixin, View):

    def get(self, request):
        
        cart = get_object_or_404(Cart, user=request.user, paid=False)
        clean_cart(cart)

        if cart.orders.count() == 0:
            messages.error(request, 'سبد خرید شما خالیست')
            return redirect('account:cart')
        
        if out_of_stock(cart, request):
            return redirect('account:cart')

        amount = cart.total_price()
        data = {
            "MerchantID": config('MERCHANT'),
            "Amount": amount,
            "Description": f'پرداخت محصولات به مبلغ کل {amount} تومان',
            "Phone": cart.user.phone_number,
            "CallbackURL": f'http://localhost:8000/api/accounts/payment-verify/?order_code={cart.order_code}&user={request.user.id}',
        }
        
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return JsonResponse({
                        'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']
                    })
                else:
                    return JsonResponse({'status': False, 'code': str(response['Status'])})
            return JsonResponse(response)
        
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})



class PaymentVerifyView(View):

    def get(self, request):
        user = get_object_or_404(User, id=request.GET.get('user', None))
        request.user = user
        authority = request.GET.get('Authority')
        cart = get_object_or_404(Cart, user=request.user, paid=False)
        amount = cart.total_price()

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
                after_payment(cart, amount, request)
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

