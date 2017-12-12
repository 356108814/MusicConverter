# encoding: utf-8
"""
缓存
@author Yuriseus
@create 2016-8-1 14:42
"""
import redis
import settings


class Cache(object):
    def __init__(self):
        self._redis = None

    def get_redis(self):
        if not self._redis:
            conf = settings.CONF['cache']
            self._redis = redis.StrictRedis(host=conf['host'], port=conf['port'], db=conf['db'])
        return self._redis

    @staticmethod
    def instance():
        if not hasattr(Cache, "_instance"):
            Cache._instance = Cache()
        return Cache._instance

    @staticmethod
    def current():
        return Cache.instance().get_redis()

