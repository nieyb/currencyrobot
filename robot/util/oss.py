# -*- coding: utf-8 -*-
_author_ = 'chenchuchuan'

import oss2
import time
from random import randint
import StringIO, re, os
from config import Access_Key_ID, Access_Key_Secret, endpoint, bucket_name


auth = oss2.Auth(Access_Key_ID, Access_Key_Secret)
service = oss2.Service(auth, endpoint)

bucket = oss2.Bucket(auth, endpoint, bucket_name)


def upload_file_to_oss(from_file_url, upload_url):
    """上传文件到oss服务器"""
    success = False
    try:
        with open(from_file_url, 'rb') as fileobj:
            success = bucket.put_object(upload_url, fileobj)
    except Exception, e:
        pass
    return success


def upload_file_images_to_oss(file, upload_url):
    """上传文件到oss服务器(StringIO)"""
    success = False
    try:
        # bucket.put_object(upload_url, file.getvalue())
        bucket.put_object(upload_url, file)
        success = True
    except Exception, e:
        pass
    return success


def itchat_upload_images_to_oss(file):
    """上传文件到oss服务器(StringIO)"""
    from config import oss_url_1, oss_url_2
    file_name = get_random_name("png")
    upload_url = oss_url_2 + file_name
    url_name_1 = oss_url_1 + file_name
    try:
        bucket.put_object(upload_url, file)
        show_url = url_name_1
    except Exception, e:
        print "====Exception========", e
        show_url = ""
    return show_url


def upload_PIL_to_oss(img, upload_url):
    """上传文件到oss服务器(PIL)"""

    sio = StringIO.StringIO()
    img.save(sio, "JPEG")
    success = False
    try:
        bucket.put_object(upload_url, sio.getvalue())
        success = True
    except Exception, e:
        print e
    return success


def delete_file_from_oss(upload_url):
    """从oss服务器删除文件"""
    if upload_url.startswith('oss://'):
        remote_upload_url = upload_url.replace('oss:///', '')
    else:
        remote_upload_url = upload_url
    success = False
    try:
        bucket.delete_object(remote_upload_url)
        success = True
    except Exception, e:
        pass
    return success


def download_file_from_oss(upload_url):
    """从服务器oss下载文件"""
    return bucket.get_object_to_file('touxiang.jpg', '头像.jpg')


def get_random_name(file_type):
    """随机生成文件名称"""
    p = '%.4f' % time.time()
    return '%s%d%s%s' % (p.replace('.', ''), randint(1, 1000), '.', file_type)
