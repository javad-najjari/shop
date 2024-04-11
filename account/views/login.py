import random
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import login
from ..models import User, OTPCode
from utils import is_valid_phone_number, permission_to_send_sms, english_numbers_converter, get_next_url




class UserLoginView(View):
    template_name = 'account/login.html'

    def get(self, request):
        next = request.GET.get('next', reverse('product:home'))
        request.session['next_url'] = next
        return render(request, self.template_name)

    def post(self, request):

        phone_number = english_numbers_converter(request.POST.get('phone_number', None))
        code = english_numbers_converter(request.POST.get('code', None))


        if phone_number:
            if not is_valid_phone_number(phone_number):
                return JsonResponse({'result': False})
            
            request.session['phone_number'] = phone_number
            
            if not permission_to_send_sms(phone_number):
                return JsonResponse({'result': True})

            code = random.randint(10000, 99999)
            OTPCode.objects.create(phone=phone_number, code=code)

            return JsonResponse({'result': True})
        
        
        elif code:
            phone_number = request.session.get('phone_number', None)

            otp_code = OTPCode.objects.filter(phone=phone_number, code=code).first()
            if otp_code and otp_code.is_valid():
                otp_code.delete()
                user = User.objects.get_or_create(phone_number=phone_number)[0]
                login(request, user)

                try:
                    del request.session['phone_number']
                except KeyError:
                    pass
                
                return JsonResponse({'result': True, 'redirect_url': get_next_url(request)})

        return JsonResponse({'result': False})


