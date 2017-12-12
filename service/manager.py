# encoding: utf-8
"""
服务管理器
@author Yuriseus
@create 2016-12-10 23:15
"""
from .user import UserService
from .converter import Converter
from .wechat import WechatService
from .pay_code import PayCodeService


class ServiceManger(object):
    def __init__(self):
        self.user = UserService()
        self.converter = Converter()
        self.wechat = WechatService()
        self.pay_code = PayCodeService()


service_manger = ServiceManger()
