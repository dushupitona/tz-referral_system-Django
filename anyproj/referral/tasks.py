from celery import shared_task
from anyproj.celery import app

from referral.models import AuthCodeModel
from datetime import datetime, timedelta
from django.utils import timezone

import os


@app.task
def auth_code_cleaner():
    auth_codes = AuthCodeModel.objects.all()
    for code in auth_codes:
        if code.date_ended < timezone.make_aware(datetime.now()):
            code.delete()
            print(f'Code deleted!')
   