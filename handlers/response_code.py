# encoding: utf-8
"""
返回码
@author Yuriseus
@create 2016-8-4 9:52
"""
from enum import Enum


class ResponseCode(Enum):
    # 公共
    SUCCESS = (0, u'请求成功')
    FAILURE = (-1, u'请求失败')
    INVALID_ARGUMENTS = (1, u'无效的参数')
    ILLEGAL_REQUEST = (2, u'非法请求')

    # 业务接口，从100开始，每个模块占100位，如用户模块1开头
    USER_VALID_ERROR = (100, u'用户名或密码错误')


