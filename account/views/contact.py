from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from ..models import ContactUs




class ContactUsView(View):
    template_name = 'account/contact-us.html'

    def get(self, request):
        return render(request, 'account/contact-us.html')
    
    def post(self, request):
        name = request.POST.get('name', None)
        title = request.POST.get('title', None)
        text = request.POST.get('text', None)

        if not (name and title and text):
            context = {'name': name, 'title': title, 'text': text}

            if not name:
                messages.error(request, 'نام را وارد کنید')
            elif not title:
                messages.error(request, 'عنوان را وارد کنید')
            elif not text:
                messages.error(request, 'متن را وارد کنید')
            
            return render(request, 'account/contact-us.html', context=context)
        
        ContactUs.objects.create(name=name, title=title, text=text)

        messages.success(request, 'پیغام شما با موفقیت ارسال شد')
        return redirect('product:home')

