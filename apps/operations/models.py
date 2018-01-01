# _*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from carsinfo.models import CarsVideo
from users.models import UserProfile
from carsinfo.models import CarOrg


# Create your models here.

class History(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    carsVideo = models.ForeignKey(CarsVideo, verbose_name=u'收藏视频')
    userProfile = models.ForeignKey(UserProfile, verbose_name=u'所属用户')

    class Meta:
        verbose_name = u'用户历史'
        verbose_name_plural = verbose_name

    def to_dict(self):
        map = {}
        map['id'] = self.id
        map['userId'] = self.userProfile_id
        map['carsVideoId'] = self.carsVideo_id
        map['addTime'] = self.add_time.strftime('%Y/%m/%d')
        return map


class Attention(models.Model):
    car_org = models.ForeignKey(CarOrg, verbose_name=u'关注机构')
    userProfile = models.ForeignKey(UserProfile, verbose_name=u"所属用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户关注'
        verbose_name_plural = verbose_name

    def to_dict(self):
        map = {}
        map['id'] = self.id
        map['userId'] = self.userProfile_id
        map['carOrgId'] = self.car_org_id
        map['addTime'] = self.add_time.strftime('%Y/%m/%d')
        return map


class Comment(models.Model):
    userProfile = models.ForeignKey(UserProfile, verbose_name=u'所属用户')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    content = models.CharField(max_length=1024, default='', verbose_name=u'评论内容')
    parent = models.ForeignKey('self', null=True, verbose_name=u'父评论')
    carsVideo = models.ForeignKey(CarsVideo, verbose_name='所属视频', null=True, blank=True)

    class Meta:
        verbose_name = u'用户评论'
        verbose_name_plural = verbose_name

    def to_dict(self):
        map = {}
        map['id'] = self.id
        map['userId'] = self.userProfile_id
        map['content'] = self.content
        map['parentId'] = self.parent_id
        map['carsVideoId'] = self.carsVideo_id
        map['addTime'] = self.add_time.strftime('%Y/%m/%d')
        return map


class Favorite(models.Model):
    fav_type = models.IntegerField(choices=((1, u'视频'), (2, u'评论'),), default=2, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    userProfile = models.ForeignKey(UserProfile, verbose_name=u'所属用户')
    comment = models.ForeignKey(Comment, verbose_name=u'所属评论',null=True,blank=True)
    carsVideo = models.ForeignKey(CarsVideo, blank=True, null=True)


    class Meta:
        verbose_name = u'用户点赞'
        verbose_name_plural = verbose_name

    def to_dict(self):
        map = {}
        map['id'] = self.id
        map['userId'] = self.userProfile_id
        map['favType'] = self.fav_type
        map['favTypeName'] = self.get_fav_type_display()
        map['commentId'] = self.comment_id
        map['carsVideoId'] = self.carsVideo_id
        map['addTime'] = self.add_time.strftime('%Y/%m/%d')
        return map
