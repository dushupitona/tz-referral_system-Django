from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from referral.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=10, unique=True)
    invite_code = models.CharField(max_length=6, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    

    @property
    def is_staff(self):
        return self.is_superuser


# class AuthCodeModel(models.Model):
#     code = models.CharField(max_length=6, blank=True)
#     date_created = models.DateTimeField(_('date joined'), auto_now_add=True)
#     date_ended = models.DateTimeField(_('date ended'), default=datetime.now() + timedelta(minutes=5))



