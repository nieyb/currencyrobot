#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
BROKER_URL = 'redis://127.0.0.1:6379/6'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {
    # 'add-every-30-seconds': {
    #     'task': 'robot.qu_add.say_hello',
    #     'schedule': crontab(hour=18, minute=40),
    #     'args': (88, 99)
    # },
    # 'say-hi-5-seconds': {
    #     'task': 'robot.qu_add.say_hi',
    #     'schedule': timedelta(seconds=5)
    # },
    # 'add-friend-data-20-seconds': {
    #     'task': 'robot.service.service_handle.add_friend_chat',
    #     'schedule': crontab(hour=1, minute=30)
    # },
    # 'add-room-data-20-seconds': {
    #     'task': 'robot.service.service_handle.add_room_chat',
    #     'schedule': crontab(hour=1, minute=30)
    # }
}


# from celery.schedules import crontab
# #每天2:30调用itchat_weixin.qu_add.say_hi
# CELERYBEAT_SCHEDULE = {
#     'say-hi-5-seconds': {
#         'task': 'robot.qu_add.say_hi',
#         'schedule': crontab(hour=2, minute=30)
#     },    
# }

