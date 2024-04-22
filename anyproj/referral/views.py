from django.shortcuts import render

from django.contrib.auth.views import LoginView


# Create your views here.

# def login(request):
#     return render(request, 'referral/login.html')   



def login(request):
    return render(request, 'referral/login.html')