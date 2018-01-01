# _*_ coding:utf-8 _*_
import json
import re

import urllib
from django.http import HttpResponse
from pure_pagination import Paginator

from Constant import AJAX_HEADER

__author__ = 'cztzc520'
__date__ = '17/12/21 下午1:43'

AJAX_SUCCESS_CODE = '0'
AJAX_FAIL_CODE = '5'
AJAX_TAGS_NOT_EXIST = '3'
AJAX_FOLLOWED_CDOE = '2'
AJAX_USER_NOTEXIST_CODE = '1'
AJAX_EMPTY_PAGE_CODE = '4'
AJAX_USER_NOTEXIST_MSG = 'user not exist'
AJAX_SUCCESS_MSG = 'success'
AJAX_FAIL_MSG = 'system error'
POST = 'POST'
GET = 'GET'
HTTP_RESP_TRUE = '0'
HTTP_RESP_FALSE = '1'
TRUE = '0'
FALSE = '1'

# 分页数据
DEFAULT_PAGE_SIZE = 10
DEFAULT_CUR_PAGE = 1
DEFAULT_PAGE_COUNT = 0
DEFAULT_TOTAL_COUNT = 0


class ReqDict(object):
    def __init__(self, request):
        self.dict = {}
        if request.method == 'POST':
            body = request.body

            if not body:
                pass
            else:
                unquoteBody = urllib.unquote(body)
                self._handle_str(unquoteBody)

        else:
            querySet = request.GET
            for key, value in querySet.items():
                if value:
                    self.dict[key] = value
                else:
                    self._params_to_dict(key)

    def get(self, key, default=''):
        val = self.dict.get(key, '')
        return val

    def _params_to_dict(self, str):

        subList = str.split('=')
        if len(subList) > 1:
            try:
                key = subList[0]
                value = subList[1]
                self.handler_str(key, value, self.dict)
            except Exception:
                self.dict[subList[0]] = subList[1]
        else:
            try:
                _dict = json.loads(subList[0])
                self._merge_dict(_dict, self.dict)
            except Exception:
                pass

    def _merge_dict(self, paramDict, orgDict):
        orgDict.update(paramDict)

    def _handle_str(self, str):
        if not str:
            return {}
        list = str.split('&')
        if not list:
            return {}
        for str in list:
            self._params_to_dict(str)

    def handler_str(self, str, value, ret):
        sub = str.split('[')
        if len(sub) > 1:
            newSub = []
            for i in xrange(len(sub)):
                if i == 0:
                    newSub.append(sub[i])
                else:
                    newSub.append('[' + sub[i])
        self.get_field_map(newSub, value, ret, None)

    def trim_field(self, field1):
        pattern = r'\[(\S+)\]'
        result = re.search(pattern, field1)
        if result:
            field1 = result.group(1)
        return field1

    def get_field_map(self, newSub, value, ret, list=None):
        one = 0
        two = 1
        if len(newSub) != 1:
            field1 = newSub[0]
            field2 = newSub[1]
        else:
            field1 = newSub[0]
            field2 = None

        if field2 == None:
            field1 = self.trim_field(field1)
            ret[field1] = value
        elif field2 == '[]':
            field1 = self.trim_field(field1)
            arr = ret.get(field1, [])
            if not arr:
                ret[field1] = arr
            try:
                field3 = newSub[two + 1]
                sub = newSub[2:]
                self.get_field_map(sub, value, ret, arr)
            except Exception:
                arr.append(value)
        else:
            # sub = newSub[1:]
            # field1 = self.trim_field(field1)
            # newRet = ret.get(field1, {})
            # if not newRet:
            #     ret[field1] = newRet
            # self.get_field_map(sub, value, newRet)
            sub = newSub[1:]
            field1 = self.trim_field(field1)
            newRet = ret.get(field1, {})
            if not newRet:
                if list != None:
                    list.append(newRet)
                else:
                    ret[field1] = newRet

            self.get_field_map(sub, value, newRet)


def set_page_info(page, ret, pageSize=DEFAULT_PAGE_SIZE, curPage=DEFAULT_CUR_PAGE
                  ,pageName='pageInfo',pageSizeName='pageSize', curPageName='curPage'):
    pageInfo = {}
    pageInfo[pageSizeName] = pageSize
    pageInfo[curPageName] = curPage

    if isinstance(page, Paginator):
        pageInfo['pageCount'] = page.num_pages
        pageInfo['totalCount'] = page.count
        try:
            if curPage < page.num_pages:
                pageInfo['hasNext'] = TRUE
            else:
                pageInfo['hasNext'] = FALSE
            if curPage > 1:
                pageInfo['hasPrevious'] = TRUE
            else:
                pageInfo['hasPrevious'] = FALSE
        except Exception as e:
            print e


    ret[pageName] = pageInfo


def ajax_success(ret={}, code=AJAX_SUCCESS_CODE, msg=AJAX_SUCCESS_MSG):
    ret['code'] = code
    ret['msg'] = msg
    return ret


def ajax_fail(ret={}, code=AJAX_FAIL_CODE, msg=AJAX_FAIL_MSG):
    return ajax_success(ret, code, msg)


def ajax_user_not_exist(ret={}, code=AJAX_USER_NOTEXIST_CODE, msg=AJAX_USER_NOTEXIST_MSG):
    return ajax_fail(ret, code, msg)


def create_ajax_res(ret):
    return HttpResponse(content=json.dumps(ret), content_type=AJAX_HEADER)


def create_ajax_cors_res(ret):
    resp = create_ajax_res(ret)
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Allow-Methods'] = 'POST,GET'
    resp['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


def get_params(request):
    return ReqDict(request)


if __name__ == '__main__':
    str = 'code=sdf&data=%7B%22content%22%3A%22dfg%22%7D'
