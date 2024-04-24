from __future__ import unicode_literals

from django.conf import settings

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from referral.managers import UserManager

from phonenumber_field.modelfields import PhoneNumberField

from datetime import datetime, timedelta

import random
import string

def generate_auth_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=14, unique=True)
    referral_code = models.CharField(max_length=6, default=generate_auth_code)
    inviter = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number' 
    REQUIRED_FIELDS = []
    

    @property
    def is_staff(self):
        return self.is_superuser
    


class AuthCodeModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(default=datetime.now() + timedelta(minutes=5))

    def __str__(self):
        return self.user.phone_number


