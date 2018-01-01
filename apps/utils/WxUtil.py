# _*_ coding:utf-8 _*_
__author__ = 'cztzc520'
__date__ = '17/12/20 下午3:57'

from weixin import WXAPPAPI
from Constant import WX_APP_ID, WX_APP_SECRET
from WXBizDataCrypt import WXBizDataCrypt
from demo import main
from weixin.client import WeixinAPI


def get_session_info(code):
    api = WXAPPAPI(appid=WX_APP_ID, app_secret=WX_APP_SECRET)
    session_info = api.exchange_code_for_access_token(code=code)
    return session_info


def get_session_key(code):
    session_info = get_session_info(code)
    return session_info['session_key']


def get_open_id(code):
    session_info = get_session_key(code=code)
    return session_info['open_id']


def get_user_info(code, encryptedData, iv):
    session_key = get_session_key(code)
    crypt = WXBizDataCrypt(appId=WX_APP_ID, sessionKey=session_key)
    return crypt.decrypt(encryptedData=encryptedData,iv=iv)

def test_get_user_info(encryptedData, iv):
    return main()

