# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-05 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='nick_name',
            field=models.TextField(default='', max_length=100),
        ),
    ]
