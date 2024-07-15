from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from utils import get_user_cart, get_user_address_information, out_of_stock
from django.contrib.auth.mixins import LoginRequiredMixin




class CheckoutView(LoginRequiredMixin, View):
    
    def get(self, request):
        context = {}
        user = self.request.user
        cart = get_user_cart(user)

        if cart.empty_orders():
            messages.error(request, 'سبد خرید شما خالیست')
            return redirect('account:cart')

        orders = cart.orders.all()
        context['cart'] = cart
        context['orders'] = orders.filter(quantity__gt=0).order_by('product_size_color__product__title')

        if out_of_stock(cart, request):
            return redirect('account:cart')


        current_cart = user.carts.filter(paid=False).last()
        previous_cart = user.carts.filter(paid=True).last()
        
        context['information'] = get_user_address_information(user, current_cart, previous_cart)

        return render(request, 'account/checkout.html', context=context)

    def post(self, request):
        user = request.user
        data = request.POST
        
        recipient_name = data.get('recipient_name')
        phone = data.get('phone')
        city = data.get('city')
        address = data.get('address')
        postal_code = data.get('postal_code')
        description = data.get('description')

        if not (recipient_name and phone and city and address):
            messages.error(request, 'فیلدهای ضروری را پر کنید')
            return redirect('account:checkout')
        elif not (phone.isdigit() and (postal_code.isdigit() if postal_code else True)):
            messages.error(request, 'شماره تلفن و کدپستی باید عدد باشند')
            return redirect('account:checkout')
        elif city not in ['گرمه', 'جاجرم', 'ایور', 'درق']:
            messages.error(request, 'شهر انتخابی اشتباه است')
            return redirect('account:checkout')
        
        cart = user.carts.filter(paid=False).last()

        cart.order_description = description
        cart.address = address
        cart.postal_code = postal_code
        cart.recipient_name = recipient_name
        cart.phone_number = phone
        cart.save()
        
        return redirect('account:payment')

