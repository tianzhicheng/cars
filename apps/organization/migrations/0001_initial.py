# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-19 17:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u673a\u6784\u540d\u79f0')),
                ('desc', models.TextField(verbose_name='\u673a\u6784\u63cf\u8ff0')),
                ('click_nums', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6570')),
                ('attention_nums', models.IntegerField(default=0, verbose_name='\u5173\u6ce8\u6570')),
                ('image', models.ImageField(upload_to='org/%Y/%m', verbose_name='\u5c01\u9762')),
                ('address', models.CharField(max_length=150, verbose_name='\u673a\u6784\u5730\u5740')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '\u6c7d\u8f66\u673a\u6784',
                'verbose_name_plural': '\u6c7d\u8f66\u673a\u6784',
            },
        ),
    ]