# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-20 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='open_id',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='openId'),
        ),
    ]
