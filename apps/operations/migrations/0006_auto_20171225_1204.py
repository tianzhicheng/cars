# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-25 12:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0005_auto_20171225_1140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='cars',
            new_name='carsVideo',
        ),
    ]
