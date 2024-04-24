from django.contrib import admin
from django.urls import path

from api.views import UserProfileAPIVIew, EnterInviteAPIVIew, send_me_code, auth

app_name = 'api'

urlpatterns = [
    path('profile/', UserProfileAPIVIew.as_view()),
    path('profile/invite_code/', EnterInviteAPIVIew.as_view()),  
    path('send_code/', send_me_code),
    path('auth/', auth),
]