# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-31 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0007_comment_carsvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='operations.Comment', verbose_name='\u6240\u5c5e\u8bc4\u8bba'),
        ),
    ]