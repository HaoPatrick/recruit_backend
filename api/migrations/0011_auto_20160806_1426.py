# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-06 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_department_nick_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personinfo',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
