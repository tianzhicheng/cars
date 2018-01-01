"""cars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from users.views import TestView
from wxoperation.views import UserLoginView,UserRegisterView,\
    CarsSearchView,HandpickView,AttentionView,\
    CarsOrgView,MyAttentionView,MyFavoriteView,MyHistoryView,MyCommentView,TagsView,\
    AddAttentionView,AddFavoriteView,AddHistoryView,TestView,CarsVideoView,AddCommentView,\
    CommentsView,CarsViedowDetailsView




import xadmin

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index1.html'), name='index'),

    url(r'^register/$', UserRegisterView.as_view(), name='register'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^getTags/$', TagsView.as_view(), name='getTags'),
    url(r'^carsSearch/$', CarsSearchView.as_view(), name='carsSearch'),
    url(r'^handpick/$', HandpickView.as_view() ,name='handpick'),
    url(r'^attention/$', AttentionView.as_view(), name='attention'),
    url(r'^carsOrg/$', CarsOrgView.as_view(), name='carsOrg'),
    url(r'^org/$', CarsOrgView.as_view(), name='org'),
    url(r'^carsViedeos',CarsVideoView.as_view(), name='carsVideos'),
    url(r'^myAttention/$', MyAttentionView.as_view() ,name='myAttention'),
    url(r'^myHistory/$', MyHistoryView.as_view(),name='myHistory'),
    url(r'^myFavorite/$', MyFavoriteView.as_view(),name='myFavorite'),
    url(r'^myComment/$', MyCommentView.as_view(),name='myComment'),
    url(r'^addAttention/$', AddAttentionView.as_view(), name='addAttention'),
    url(r'^addFavorite/$',AddFavoriteView.as_view(), name='myFavorite'),
    url(r'^addHistory/$', AddHistoryView.as_view(), name='addFavorite'),
    url(r'^addComment/$', AddCommentView.as_view(), name='addComment'),
    url(r'^comments/$', CommentsView.as_view(), name='comments'),
    url(r'^carsViedowDetails', CarsViedowDetailsView.as_view(), name='carsViedowDetails'),
    url(r'getTest/$', TestView.as_view(), name='addTest')
]
