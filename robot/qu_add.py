# -*- coding:utf-8 -*-
from celery_config import cry
import datetime

@cry.task
def say_hello(n, m):
    for i in range(n):
        print "====================msg================"
        print i

@cry.task
def say_hi():
	print "============hi================"
	time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print "time now: ", time_now

