# Generated by Django 5.0.4 on 2024-04-24 16:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0012_alter_authcodemodel_date_ended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authcodemodel',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 24, 16, 24, 47, 293281)),
        ),
    ]
