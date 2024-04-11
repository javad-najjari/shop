import random
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from ..models import User
from utils import is_valid_phone_number, permission_to_send_sms
from ..models import OTPCode




class SendVerificationCodeView(View):
    template_name = 'account/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        import time
        time.sleep(2)

        phone_number = request.POST.get('phone_number', None)

        if not is_valid_phone_number(phone_number):
            print('=' * 50)
            print('phone number is not valid')
            print('=' * 50)
            return JsonResponse({'result': False})
        
        if not permission_to_send_sms(phone_number):
            return JsonResponse({})

        code = random.randint(10000, 99999)
        OTPCode.objects.create(phone=phone_number, code=code)

        return JsonResponse({'result': True})



class UserLoginView(View):

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user != None:
                login(request, user)
                return redirect('store:home')
                
            return redirect('accounts:login')
        

