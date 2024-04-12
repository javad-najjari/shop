from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin




class ProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        request.user.name = name
        request.user.save()
        return JsonResponse({})

