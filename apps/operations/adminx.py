# _*_ coding:utf-8 _*_
__author__ = 'cztzc520'
__date__ = '17/12/19 上午10:13'

from .models import Favorite, Comment, History, Attention
import xadmin


class FavoriteAdmin(object):
    list_display = ['fav_type', 'userProfile', 'add_time']
    search_fields = ['fav_type', 'userProfile']
    list_filter = ['fav_type', 'userProfile', 'add_time']


class CommentAdmin(object):
    list_display = ['userProfile', 'parent', 'add_time']
    search_fields = ['userProfile', 'parent']
    list_filter = ['userProfile', 'parent', 'add_time']


class HistoryAdmin(object):
    list_display = ['cars', 'userProfile', 'add_time']
    search_fields = ['cars', 'userProfile']
    list_filter = ['cars', 'userProfile', 'add_time']


class AttentionAdmin(object):
    list_display = ['car_org', 'userProfile', 'add_time']
    search_fields = ['car_org', 'userProfile']
    list_filter = ['car_org', 'userProfile', 'add_time']


xadmin.site.register(Favorite, FavoriteAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(History, HistoryAdmin)
xadmin.site.register(Attention, AttentionAdmin)
