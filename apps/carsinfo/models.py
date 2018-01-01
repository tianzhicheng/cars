# _*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from organization.models import CarOrg


# Create your models here.
from utils.QiniuUtil import QiniuStorage


class Tags(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'标签名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def __unicode__(self):
        return self.name

    def to_dict(self):
        map = {}
        map['name'] = self.name
        return map

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = verbose_name


class CarsVideo(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'视频名')
    desc = models.CharField(max_length=300, verbose_name=u'视频描述')
    url = models.URLField(max_length=150, verbose_name=u'视频链接')
    duration = models.IntegerField(default=0, verbose_name=u'时长')
    play_nums = models.IntegerField(default=0, verbose_name=u'播放数')
    cover = models.ImageField(upload_to='video/%Y/%m',storage=QiniuStorage(), verbose_name=u'封面')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    carsOrg = models.ForeignKey(CarOrg, verbose_name=u'所属机构')
    tags = models.ManyToManyField(Tags, verbose_name=u'标签', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def to_dict(self):
        map = {}
        map['id'] = self.id
        map['name'] = self.name
        map['desc'] = self.desc
        map['url'] = self.url
        map['duration'] = self.duration
        map['cover'] = self.cover.name
        map['playNums'] = self.play_nums
        map['addTime'] = self.add_time.strftime('%Y/%m/%d')
        return map

    class Meta:
        verbose_name = u'视频资源'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
