# encoding: utf-8
"""
拦截器接口
@author Yuriseus
@create 2016-8-3 15:30
"""
from abc import ABCMeta, abstractmethod


class Interceptor(metaclass=ABCMeta):
    def init(self):
        pass

    @abstractmethod
    def intercept(self, handler):
        pass

    def destroy(self):
        pass
