# _*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


# Create your models here.
from utils.QiniuUtil import QiniuStorage


class CarOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    attention_nums = models.IntegerField(default=0, verbose_name=u'关注数')
    image = models.ImageField(upload_to='org/%Y/%m', storage=QiniuStorage(),verbose_name=u'封面')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'汽车机构'
        verbose_name_plural = verbose_name

    def to_dict(self):
        map = {}
        map['id'] = self.id
        map['name'] = self.name
        map['desc'] = self.desc
        map['clickNums'] = self.click_nums
        map['attentionNums'] = self.attention_nums
        map['image'] = self.image.name
        map['address'] = self.address
        map['addTime'] = self.add_time.strftime('%Y/%m/%d')
        return map
