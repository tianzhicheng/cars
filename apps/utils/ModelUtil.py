# _*_ coding:utf-8 _*_
__author__ = 'cztzc520'
__date__ = '17/12/21 下午4:05'

import json


def to_list_dict(models):
    vs = []
    if models:
        for v in models:
            m_dict = v.to_dict()
            vs.append(m_dict)
    return vs


if __name__ == '__main__':
    ret = {}
    list = []
    ret['list'] = list
    print json.dumps(ret)
