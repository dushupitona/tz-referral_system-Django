from django.contrib import admin
from django.urls import path

from api.views import UsersListAPIVIew, send_me_code, auth

app_name = 'api'

urlpatterns = [
    path('users/', UsersListAPIVIew.as_view()),
    path('send_code/', send_me_code),
    path('auth/', auth),
]