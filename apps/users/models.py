# _*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nickName = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default='female', max_length=10)
    address = models.CharField(max_length=100, default=u'')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name=u'城市', default='')
    province = models.CharField(max_length=50, verbose_name=u'省份', default='')
    avatarUrl = models.CharField(max_length=200, verbose_name=u'地址', default='')
    image = models.ImageField(upload_to='image/%Y/%m', default=u'image/default.png', max_length=100)
    openId = models.CharField(max_length=50, unique=True, verbose_name=u'openId', default='')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nickName

    def to_dict(self):
        map = {}
        map['id'] = self.id
        map['nickName'] = self.nickName
        map['gender'] = self.get_gender_display()
        map['city'] = self.city
        map['mobile'] = self.mobile
        map['province'] = self.province
        map['openId'] = self.openId
        return map
