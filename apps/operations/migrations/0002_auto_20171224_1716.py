# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-24 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attention',
            options={'verbose_name': '\u7528\u6237\u5173\u6ce8', 'verbose_name_plural': '\u7528\u6237\u5173\u6ce8'},
        ),
        migrations.RenameField(
            model_name='favorite',
            old_name='user',
            new_name='userProfile',
        ),
        migrations.RenameField(
            model_name='history',
            old_name='user',
            new_name='userProfile',
        ),
    ]
