# encoding: utf-8
"""
项目配置
@author Yuriseus
@create 2016-8-3 11:34
"""
import os

DEBUG = True
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

XHEADERS = True
# 静态文件路径
STATIC_PATH = os.path.join(BASE_PATH, 'static')

# 模板路径
TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')

# 拦截器
INTERCEPTOR_CLASSES = [
    'interceptor.auth.AuthInterceptor'
]

DEFAULT_CON_PATH = 'conf/default.conf'

# 包含字典的字典，解析自DEFAULT_CON_PATH
CONF = {}

