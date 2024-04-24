from celery import shared_task
from anyproj.celery import app

from referral.models import AuthCodeModel
from datetime import datetime
from django.utils import timezone

import random
import time


@app.task
def auth_code_cleaner():
    auth_codes = AuthCodeModel.objects.select_related('user').all()
    for code in auth_codes:
        if code.date_ended < timezone.make_aware(datetime.now()):
            code.delete()
            print(f'Code deleted!')
            if not code.user.is_active:
                code.user.delete()
                print(f'Inactive user deleted!')
   

@shared_task
def send_auth_code(user_id):
    try:
      time.sleep(2)
      code = str(random.randint(1000, 9999))
      print(code)
      new_code = AuthCodeModel.objects.create(user_id=user_id, code=code)
      new_code.save()
      print(f'Code for id: {user_id} created !')
      print(f'\n CODE: {code} \n')
    except:
        print(f'Code for id: {user_id} already exist !')