from django.contrib import admin

from referral.models import User, AuthCodeModel

# Register your models here.

    
admin.site.register(User)
admin.site.register(AuthCodeModel)