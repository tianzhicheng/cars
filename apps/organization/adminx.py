# _*_ coding:utf-8 _*_
__author__ = 'cztzc520'
__date__ = '17/12/19 上午10:00'

from .models import CarOrg
import xadmin


class CarOrgAdmin(object):
    list_display = ['name', 'click_nums', 'attention_nums', 'address', 'add_time', 'desc']
    search_fields = ['name', 'attention_nums', 'address']
    list_filter = ['name', 'click_nums', 'attention_nums', 'address', 'add_time', 'desc']


xadmin.site.register(CarOrg, CarOrgAdmin)
