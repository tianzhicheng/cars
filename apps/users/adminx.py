# _*_ coding:utf-8 _*_
__author__ = 'cztzc520'
__date__ = '17/12/18 上午11:30'

import xadmin
from xadmin import views
from .models import UserProfile


class BaseSetting(object):
    enable_thems = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = u'王华奇大傻逼'
    site_footer = u'爆点传媒'
    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
