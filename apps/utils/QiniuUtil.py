# _*_ coding:utf-8 _*_
from django.core.files.storage import Storage

__author__ = 'cztzc520'
__date__ = '17/12/27 下午5:15'

from qiniu import Auth, put_file, etag, urlsafe_base64_decode, put_data
from datetime import datetime
import qiniu.config
import uuid

access_key = 'S1OJnp4zGGESPpIk8T5xgX7JmIFBqSXvAZ0Ctmni'
secret_key = 'xajk935ZMnfSHLwZ844OT3qxVPMOAFjCDnLc-6MB'
image_bucket_name = 'image'
video_bucket_name = 'video'
img_file_prefix = 'http://p1m4hjep7.bkt.clouddn.com/'
video_file_prefix = 'http://p1k01d93z.bkt.clouddn.com/'

localfile = '/Users/cztzc520/djangoVir/cars/org/2017/12/20160721_180633.jpg'


class QiniuStorage(Storage):
    def _save(self, name, content):
        fileName = upload_img(content)
        if fileName == '':
            raise Exception('image system error')
        return fileName

    def exists(self, name):
        return False

    def path(self, name):
        return name

    def url(self, name):
        return name


def _get_token(key, type=image_bucket_name):
    q = Auth(access_key=access_key, secret_key=secret_key)
    token = q.upload_token(type, key, 3600)
    return token


def generate_file_name(suffix='jpg'):
    # dateStr = datetime.now().strftime('%Y-%m-%d-')
    uuidStr = uuid.uuid1().hex
    return uuidStr + '.' + suffix


def upload_by_url(file, type=image_bucket_name):
    ret_str = ''
    try:
        suffix = file.split('.')[1]
        fileName = generate_file_name(suffix)
        token = _get_token(fileName, type)
        put_file(token, fileName, 3600)
        return img_file_prefix + fileName

    except Exception:
        pass
    return ret_str


def upload_by_bys(file, type=image_bucket_name):
    ret_str = ''
    try:
        suffix = str(file.name).split('.')[1]
        name = generate_file_name(suffix)
        _get_token(name, type)
        token = _get_token(name, type)
        ret, info = put_data(token, name, file.read())
        if info.status_code == 200:
            return img_file_prefix + name
    except Exception as e:
        print e
    return ret_str


def upload_img(file, type=image_bucket_name):
    if isinstance(file, str):
        ret = upload_by_url(file, type)
    else:
        ret = upload_by_bys(file, type)
    return ret


def upload_video(file, type=video_bucket_name):
    return upload_img(file, type)
