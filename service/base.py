# encoding: utf-8
"""
基础业务类，数据库操作使用sqlalchemy
@author Yuriseus
@create 2016-8-3 20:10
"""
from coffeebean.log import logger
from coffeebean.cache import Cache
from coffeebean.db import SQLAlchemy


class BaseService(object):
    def __init__(self):
        self.logger = logger
        self.cache = Cache.current()
        self.db = SQLAlchemy.instance()


