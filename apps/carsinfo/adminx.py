# _*_ coding:utf-8 _*_
__author__ = 'cztzc520'
__date__ = '17/12/19 下午3:46'

from .models import CarsVideo, Tags
import xadmin


class CarsVideoAdmin(object):
    list_display = ['name', 'tags','url', 'duration', 'play_nums', 'carsOrg', 'add_time', 'desc']
    search_fields = ['name', 'tags','url', 'duration', 'play_nums', 'carsOrg']
    list_filter = ['name', 'tags','url', 'duration', 'play_nums', 'carsOrg', 'add_time']


class TagsAdmin(object):
    list_display = ['name',  'add_time']
    search_fields = ['name', ]
    list_filter = ['name',  'add_time']

xadmin.site.register(CarsVideo, CarsVideoAdmin)
xadmin.site.register(Tags, TagsAdmin)
