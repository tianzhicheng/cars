# _*_coding:utf-8_*_
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from pure_pagination import Paginator

from users.models import UserProfile as User
from carsinfo.models import CarsVideo, Tags
from organization.models import CarOrg
from operations.models import Comment, History, Favorite, Attention
from utils import WxUtil, HttpUtil
from utils.Constant import AJAX_HEADER
from django.core import serializers
from utils.ModelUtil import to_list_dict
import json


# Create your views here.
# 用户登录
class UserLoginView(View):
    def post(self, request):
        ret = {}
        data = {}
        dict = HttpUtil.ReqDict(request)
        code = dict.get("code", '')
        encrypted_data = dict.get("encryptedData", '')
        iv = dict.get("iv", '')
        # user_info = WxUtil.get_user_info(code, encryptedData=encrypted_data, iv=iv)
        user_info = WxUtil.test_get_user_info(encrypted_data, iv)
        # open_id = WxUtil.get_open_id(code)
        open_id = '2'
        # open_id = user_info.get('openId', '')
        user = User.objects.filter(openId=open_id)
        data['userInfo'] = user_info
        ret['data'] = data
        data['openId'] = open_id
        if user:
            HttpUtil.ajax_success(ret)
            return HttpResponse(content=json.dumps(ret), content_type=AJAX_HEADER)
        else:
            HttpUtil.ajax_user_not_exist(ret)
            return HttpResponse(content=json.dumps(ret), content_type=AJAX_HEADER)


# 用户注册
class UserRegisterView(View):
    def post(self, request):
        ret = {}
        data = {}
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        userInfo = dict.get('userInfo', {})
        user = User.objects.filter(openId=openId)
        if user.exists():
            HttpUtil.ajax_fail(ret, msg='the user is already register')
            data['user'] = user[0].to_dict()
            ret['data'] = data
            return HttpResponse(content=json.dumps(ret), content_type=AJAX_HEADER)
        else:
            newUser = User()
            newUser.nickName = userInfo.get("nickName")
            newUser.gender = userInfo.get("gender")
            newUser.city = userInfo.get("city")
            newUser.province = userInfo.get("province")
            newUser.openId = openId
            newUser.username = openId
            newUser.avatarUrl = userInfo.get("avatarUrl")
            try:
                newUser.save()
                HttpUtil.ajax_success(ret)
                data['userInfo'] = newUser.to_dict()
                ret['data'] = data
                return HttpResponse(content=json.dumps(ret), content_type=AJAX_HEADER)
            except Exception as e:
                HttpUtil.ajax_fail(ret)
                ret['data'] = data
                return HttpResponse(content=json.dumps(ret), content_type=AJAX_HEADER)


# 用户检查 如果存在则将用户id存入ret中 并返回True
def check_user(openId, ret):
    try:
        user = User.objects.get(openId=openId)
        if user:
            ret['userId'] = user.id
            return True
    except Exception:
        pass
    HttpUtil.ajax_user_not_exist(ret)
    return False


# 用户标签查询
class TagsView(View):
    def get(self, request):
        ret = {}
        data = {}
        try:
            tags = Tags.objects.all()
            list_dict = to_list_dict(tags)
            data['tagList'] = list_dict
            nameList = []
            for d in list_dict:
                name = d.get('name', '')
                nameList.append(name)
            data['nameList'] = nameList
            ret['data'] = data
            HttpUtil.ajax_success(ret)

        except Exception as e:
            HttpUtil.ajax_fail(ret)
            ret['data'] = []
        return HttpUtil.create_ajax_res(ret)


# 视频搜索
class CarsSearchView(View):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        ret = {}
        data = {}
        dict = HttpUtil.get_params(request)
        content = dict.get('content', '')
        try:
            tag = Tags.objects.get(name=content)
            if tag is not None:
                videos = CarsVideo.objects.filter(tags=tag.id)
                data['videos'] = to_list_dict(videos)
                HttpUtil.ajax_success(ret)
        except Tags.DoesNotExist:
            videos = CarsVideo.objects.filter(name__icontains=content)
            data['videos'] = to_list_dict(videos)
            HttpUtil.ajax_success(ret)
        except Exception as e:
            HttpUtil.ajax_fail(ret)
        ret['data'] = data
        str = json.dumps(ret)
        return HttpResponse(content=json.dumps(ret), content_type=AJAX_HEADER)


# 精选
class HandpickView(View):
    # 最热
    HEAD = 0
    # 最新
    NEWEST = 1

    def post(self, request):
        ret = {}
        data = {}
        dict = HttpUtil.ReqDict(request)
        type = int(dict.get('type', self.NEWEST))
        pageSize = int(dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE))
        curPage = int(dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE))
        try:

            if type is self.HEAD:
                videos = CarsVideo.objects.all().order_by('-play_nums')
            else:
                videos = CarsVideo.objects.all().order_by('-add_time')

            p = Paginator(videos, pageSize)
            videos = p.page(curPage)
            if videos:
                videos = to_list_dict(videos.object_list)
                data['videos'] = videos
                ret['data'] = data
                HttpUtil.set_page_info(p, ret, pageSize, curPage)
                HttpUtil.ajax_success(ret)
        except EmptyPage:
            HttpUtil.set_page_info(None, ret, pageSize, curPage)
        except Exception:
            HttpUtil.ajax_fail(ret)
        return JsonResponse(ret)


class AddAttentionView(View):
    def post(self, request):
        ret = {}
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        orgId = int(dict.get('orgId', 0))
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            id = ret.get('userId', 0)
            old = Attention.objects.filter(userProfile=id, car_org=orgId)
            if old:
                HttpUtil.ajax_fail(ret, HttpUtil.AJAX_FOLLOWED_CDOE, 'the Org is already followed')
            else:
                newAttention = Attention()
                newAttention.car_org_id = openId
                newAttention.userProfile_id = id
                newAttention.save()
                HttpUtil.ajax_success(ret)
        except Exception as e:
            print e
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


def get_attention_ret(request, dict, ret, data):
    try:
        userId = ret.get('userId', 0)
        pageSize = int(dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE))
        curPage = int(dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE))
        orgs = CarOrg.objects.all()
        p = Paginator(orgs, pageSize)
        orgs = p.page(curPage)
        orgs_list = to_list_dict(orgs.object_list)
        for org in orgs_list:
            id = org.get('id', 0)
            count = CarsVideo.objects.filter(carsOrg=id).count()
            org['videoCount'] = count
            attention = Attention.objects.filter(userProfile=userId, car_org=id)
            if attention:
                org['isAttention'] = HttpUtil.HTTP_RESP_TRUE
            else:
                org['isAttention'] = HttpUtil.HTTP_RESP_FALSE
        data['orgs'] = orgs_list
        HttpUtil.set_page_info(p, ret, pageSize, curPage)
    except Exception:
        HttpUtil.set_page_info(None, ret)
        data['orgs'] = []
        HttpUtil.ajax_fail(ret)


class AttentionView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        get_attention_ret(request, dict, ret, data)
        HttpUtil.ajax_success(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class CarsOrgView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        get_attention_ret(request, dict, ret, data)
        org_list = ret.get('data').get('orgs')
        vidoesCurPage = int(dict.get('videosCurPage', 1))
        vidoedPageSize = int(dict.get('videosPageSize', 3))
        for org in org_list:
            id = int(org.get('id', 0))
            vidoes = CarsVideo.objects.filter(carsOrg=id).all()
            try:
                p = Paginator(vidoes, vidoedPageSize)
                vidoes = p.page(vidoesCurPage)
                vidoes = to_list_dict(vidoes.object_list)
                org['videos'] = vidoes

            except Exception:
                org['videos'] = []
        HttpUtil.set_page_info(None, ret, vidoedPageSize, vidoesCurPage,
                               "vidoePageInfo", 'videosPageSize', 'videosCurPage')
        str = json.dumps(ret)
        return JsonResponse(ret)


class CarsVideoView(View):
    typeDict = {}
    typeDict['0'] = u'精选'
    typeDict['1'] = u'改装'
    typeDict['2'] = u'超跑'
    typeDict['3'] = u'飘移'
    typeDict['4'] = u'新车'
    typeDict['5'] = u'媒体'

    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        type = dict.get('type', '0')

        try:
            tag = Tags.objects.filter(name=self.typeDict.get(type, u'精选'))
            if tag.exists():
                pageSize = int(dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE))
                curPage = int(dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE))
                id = tag[0].id
                videos = CarsVideo.objects.filter(tags=id).order_by('-add_time')
                p = Paginator(videos, pageSize)
                videos = p.page(curPage).object_list
                videos = to_list_dict(videos)
                data['videos'] = videos
                HttpUtil.set_page_info(p, ret, 'pageSize', 'curPage')
                HttpUtil.ajax_success(ret)
            else:
                HttpUtil.ajax_fail(ret, HttpUtil.AJAX_TAGS_NOT_EXIST, u'找不到内容对应的标签')
        except EmptyPage:
            HttpUtil.set_page_info(None, ret)
            data['videos'] = []
        except Exception as e:
            print e
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class AddFavoriteView(View):
    COMMENT = 2
    VIDEO = 1

    def post(self, request):
        ret = {}
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            resourceId = int(dict.get('resourceId', 0))
            type = int(dict.get('type', self.VIDEO))
            userId = int(ret.get('userId', 0))

            if type == self.COMMENT:
                favorite = Favorite.objects.filter(userProfile=userId, fav_type=type, comment=resourceId)

            else:
                favorite = Favorite.objects.filter(userProfile=userId, fav_type=type, carsVideo=resourceId)
            if favorite.exists():
                HttpUtil.ajax_fail(ret, '6', 'this resources is already favorited')
            else:
                newFavorite = Favorite()
                newFavorite.fav_type = type
                newFavorite.userProfile_id = userId
                if type == self.COMMENT:
                    newFavorite.comment_id = resourceId
                else:
                    newFavorite.carsVideo_id = resourceId
                newFavorite.save()
                HttpUtil.ajax_success(ret)
        except Exception as e:
            print e
            HttpUtil.ajax_fail(ret)
        str=json.dumps(ret)
        return JsonResponse(ret)


class MyFavoriteView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        userId = int(ret.get('userId', 0))
        try:
            favorites = Favorite.objects.filter(userProfile=userId, fav_type=1).order_by('-add_time')
            if favorites.exists():
                pageSize = int(dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE))
                curPage = int(dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE))
                p = Paginator(favorites, pageSize)
                favorites = p.page(curPage)
                favs = to_list_dict(favorites.object_list)
                for fav in favs:
                    id = int(fav.get('carsVideoId', 0))
                    video = CarsVideo.objects.filter(id=id)
                    if video.exists():
                        fav['video'] = video[0].to_dict()
                    else:
                        fav['video'] = {}
                data['favorites'] = favs
                HttpUtil.set_page_info(p, ret,pageSize,curPage)
                HttpUtil.ajax_success(ret)
        except EmptyPage:
            HttpUtil.ajax_fail(ret, HttpUtil.AJAX_EMPTY_PAGE_CODE, 'page is empty')
        except Exception as e:
            print e
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class AddHistoryView(View):
    def post(self, request):
        ret = {}
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            userId = int(ret.get('userId', 0))
            resourceId = int(dict.get('resourceId', 0))
            old = History.objects.filter(userProfile=userId, carsVideo=resourceId)
            if not old.exists():
                newHistory = History()
                newHistory.carsVideo_id = resourceId
                newHistory.userProfile_id = userId
                newHistory.save()
            HttpUtil.ajax_success(ret)
        except Exception:
            HttpUtil.ajax_fail(ret)
        return JsonResponse(ret)


class MyHistoryView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            userId = int(ret.get('userId', 0))
            historys = History.objects.filter(userProfile=userId).order_by('-add_time')
            if historys.exists():
                pageSize = int(dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE))
                curPage = int(dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE))
                p = Paginator(historys, pageSize)
                historys = p.page(curPage)
                historys = to_list_dict(historys.object_list)
                for h in historys:
                    carsVideoId = int(h.get('carsVideoId', 0))
                    video = CarsVideo.objects.filter(id=carsVideoId)
                    if video.exists():
                        h['video'] = video[0].to_dict()
                    else:
                        h['video'] = {}
                data['historys'] = historys
                HttpUtil.set_page_info(p, ret,pageSize,curPage)
            else:
                data['historys'] = []
            HttpUtil.ajax_success(ret)
        except EmptyPage:
            HttpUtil.ajax_fail(ret, HttpUtil.AJAX_EMPTY_PAGE_CODE, 'page is empty')
        except Exception:
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class CarsViedowDetailsView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            resouceId = int(dict.get('resourceId', 0))
            video = CarsVideo.objects.filter(id=resouceId)
            if video.exists():
                data['video'] = video[0].to_dict()
            HttpUtil.ajax_success(ret)
        except Exception:
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class MyAttentionView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            userId = ret.get('userId', '')
            pageSize = int(dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE))
            curPage = int(dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE))
            attentions = Attention.objects.filter(userProfile=userId)
            p = Paginator(attentions, pageSize)
            attentions = p.page(curPage)
            if attentions.object_list:
                attentions = to_list_dict(attentions.object_list)
                for attention in attentions:
                    carOrgId = int(attention.get('carOrgId', 0))
                    org = CarOrg.objects.filter(id=carOrgId)
                    if org.exists():
                        attention['org'] = org[0].to_dict()
                    else:
                        attention['org'] = {}
                data['attentions'] = attentions
            else:
                data['attentions'] = []
            HttpUtil.ajax_success(ret)
        except EmptyPage:
            HttpUtil.ajax_fail(ret, HttpUtil.AJAX_EMPTY_PAGE_CODE, 'page is empty')
        except Exception as e:
            print e
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class AddCommentView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            userId = int(ret.get('userId', 0))
            content = dict.get('content', '')
            if not content:
                raise Exception(u'评论内容不能为空')
            resourceId = int(dict.get('resourceId',0))
            comm = Comment()
            comm.userProfile_id = userId
            comm.content = content
            comm.carsVideo_id = resourceId
            comm.save()
            fav = Favorite()
            fav.comment_id = comm.id
            fav.fav_type = 2
            fav.userProfile_id = userId
            fav.save()
            data['comment'] = comm.to_dict()
            HttpUtil.ajax_success(ret)
        except Exception:
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class MyCommentView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            userId = int(ret.get('userId', 0))
            pageSize = dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE)
            curPage = dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE)
            comments = Comment.objects.filter(userProfile=userId)
            p = Paginator(comments, pageSize)
            comments = p.page(curPage).object_list
            if comments:
                data['comments'] = comments
            else:
                data['comments'] = {}
            HttpUtil.set_page_info(p, ret)
            HttpUtil.ajax_success(ret)
        except EmptyPage:
            HttpUtil.ajax_fail(ret, HttpUtil.AJAX_EMPTY_PAGE_CODE, 'page is empty')
        except Exception:
            HttpUtil.ajax_fail(ret)
        return JsonResponse(ret)


class CommentsView(View):
    def post(self, request):
        ret = {}
        data = {}
        ret['data'] = data
        dict = HttpUtil.ReqDict(request)
        openId = dict.get('openId', '')
        if not check_user(openId, ret):
            return JsonResponse(ret)
        try:
            userId = int(ret.get('userId', 0))
            resourceId = int(dict.get('resourceId', 0))
            pageSize = int(dict.get('pageSize', HttpUtil.DEFAULT_PAGE_SIZE))
            curPage = int(dict.get('curPage', HttpUtil.DEFAULT_CUR_PAGE))
            comments = Comment.objects.filter(carsVideo=resourceId)
            if comments.exists():
                p = Paginator(comments, pageSize)
                comments = p.page(curPage)
                comments = comments.object_list
                data['comments'] = comments
                HttpUtil.set_page_info(p, ret)
                comments = to_list_dict(comments)
                for comm in comments:
                    commId = int(comm.get('id', 0))
                    fav = Favorite.objects.filter(comment=commId, userProfile=userId, fav_type=2)
                    if fav.exists():
                        comm['isFavorite'] = '1'
                data['comments'] = comments
                HttpUtil.set_page_info(p, ret, pageSize, curPage)
            else:
                HttpUtil.set_page_info(None, ret)
                data['comments'] = {}
            HttpUtil.ajax_success(ret)
        except EmptyPage:
            HttpUtil.ajax_fail(ret, HttpUtil.AJAX_EMPTY_PAGE_CODE, 'page is empty')
        except Exception:
            HttpUtil.ajax_fail(ret)
        str = json.dumps(ret)
        return JsonResponse(ret)


class TestView(View):
    def get(self, request):
        for c in CarOrg.objects.all():
            print c.to_dict()
