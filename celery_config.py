# -*- coding:utf-8 -*-
""" 启动队列
cd weixin_jiqiren/robot
不加入定时启动：
celery worker -A celery_config -l info -c 5

加入定时启动:
celery worker -A celery_config -l info -c 5 -B
"""
from celery import Celery

cry = Celery('celery_config', include=['robot.service.service_handle'])

cry.config_from_object('celerys')