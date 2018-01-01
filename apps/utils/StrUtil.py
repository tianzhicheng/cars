# _*_ coding:utf-8 _*_
__author__ = 'cztzc520'
__date__ = '17/12/29 上午10:52'
import re

str = 'userInfo[province]=Guangdong&userInfo[openId]=oGZUI0egBJY1zhBYw2KhdUfwVJJE&userInfo[language]=zh_CN&userInfo[city]=Guangzhou&userInfo[gender]=1&userInfo[avatarUrl]=http://wx.qlogo.cn/mmopen/vi_32/aSKcBBPpibyKNicHNTMM0qJVh8Kjgiak2AHWr8MHM4WgMEm7GFhsf8OYrySdbvAMvTsw3mo8ibKicsnfN5pRjl1p8HQ/0&userInfo[watermark][timestamp]=1477314187&userInfo[watermark][appid]=wx4f4bc4dec97d474b&userInfo[country]=CN&userInfo[nickName]=Band&userInfo[unionId]=ocMvos6NjeKLIBqg5Mr9QjxrP1FA&userInfo[item][data]=1&userInfo[item][value]=a&user[province]=Guangdong&user[openId]=oGZUI0egBJY1zhBYw2KhdUfwVJJE&user[language]=zh_CN&user[city]=Guangzhou&user[gender]=1&user[avatarUrl]=http://wx.qlogo.cn/mmopen/vi_32/aSKcBBPpibyKNicHNTMM0qJVh8Kjgiak2AHWr8MHM4WgMEm7GFhsf8OYrySdbvAMvTsw3mo8ibKicsnfN5pRjl1p8HQ/0&user[watermark][timestamp]=1477314187&user[watermark][appid]=wx4f4bc4dec97d474b&user[country]=CN&user[nickName]=Band&user[unionId]=ocMvos6NjeKLIBqg5Mr9QjxrP1FA&user[item][data]=1&user[item][value]=a&openId=2'


def handler_str(str, value, ret):
    sub = str.split('[')
    if len(sub) > 1:
        newSub = []
        for i in xrange(len(sub)):
            if i == 0:
                newSub.append(sub[i])
            else:
                newSub.append('[' + sub[i])
    get_field_map(newSub, value, ret, None)
    print ret


def trim_field(field1):
    pattern = r'\[(\S+)\]'
    result = re.search(pattern, field1)
    if result:
        field1 = result.group(1)
    return field1


def get_field_map(newSub, value, ret, list=None):
    one = 0
    two = 1
    if len(newSub) != 1:
        field1 = newSub[one]
        field2 = newSub[two]
    else:
        field1 = newSub[one]
        field2 = None

    if field2 == None:
        field1 = trim_field(field1)
        ret[field1] = value
    elif field2 == '[]':
        field1 = trim_field(field1)
        arr = ret.get(field1, [])
        if not arr:
            ret[field1] = arr
        try:
            field3 = newSub[two + 1]
            sub = newSub[2:]
            get_field_map(sub, value, ret, arr)
        except Exception:
            arr.append(value)

    else:
        sub = newSub[1:]
        field1 = trim_field(field1)
        newRet = ret.get(field1, {})
        if not newRet:
            if list != None:
                list.append(newRet)
            else:
                ret[field1] = newRet

        get_field_map(sub, value, newRet)


if __name__ == '__main__':
    # str = 'user[item][value]'
    # str = 'user[openId]=oGZU&user[language]=zh_CN&user[city]=Guangzhou&user[gender]=1&user[watermark][appid]=wx4f4bc4dec97d474b&user[watermark][id]=wx4f4bc4dec97d474b'
    str = 'user[openId][arr][][item][data]=oGZU&user[openId][arr][][item][data]=zh_CN&user[openId][arr][][item][data]=1'
    # str = 'user[openId][arr][]=oGZU&user[openId][arr][]=zh_CN&user[openId][arr][]=1'
    strList = str.split('&')
    ret = {}
    for i in strList:
        list = i.split("=")
        key = list[0]
        value = list[1]
        handler_str(key, value, ret)
    print ret
