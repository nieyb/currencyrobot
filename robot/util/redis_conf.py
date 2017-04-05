# -*- coding: utf-8 -*-

import redis
from config import redis_host, redis_port, redis_db

predis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

#predis = redis_2.pipeline()
