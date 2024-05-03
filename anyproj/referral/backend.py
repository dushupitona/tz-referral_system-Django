from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

from referral.models import AuthCodeModel

from django.db.models import Q


class AuthCodeBackend(BaseBackend):


    def authenticate(self, request, user_id=None, phone_number=None, auth_code=None):
        user_model = get_user_model()
        user = user_model.objects.get(Q(id=user_id) | Q(phone_number=phone_number))
        user_auth_code = AuthCodeModel.objects.get(user=user).code
        auth_code_valid = auth_code == user_auth_code
        if user and auth_code_valid:    
            return user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
