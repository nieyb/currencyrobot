# -*- coding: utf-8 -*-
import urllib, urllib2, requests
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

#API_KEY = '93387be801f0a430c9078c44bb91d4b7'
API_KEY = '7c1581cec73a4be38f45ed3624b6990b'
raw_TULINURL = "http://www.tuling123.com/openapi/api"


def robot_reply(info, uid=0):
    info_ = info
    #print info_
    data_ = {
        "key": API_KEY,
        "info": info_,
        "userid": str(uid)
    }
    result = requests.post(url=raw_TULINURL, data=data_)
    # print result.content
    hjson = json.loads(result.content)
    length = len(hjson.keys())
    content = hjson['text']
    print content
    return content


if __name__ == '__main__':
    info = "1123"
    robot_reply(info, uid=0)
