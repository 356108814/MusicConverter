# encoding: utf-8
"""
url路由配置
@author Yuriseus
@create 2016-8-3 14:36
"""
from tornado.web import StaticFileHandler

import settings
from handlers.index import IndexHandler
from handlers.converter import ConverterHandler
from handlers.wechat import WechatHandler
from handlers.gen_pay_code import GenPayCodeHandler
from handlers.download import DownloadHandler

handlers = [
    (r'/?', IndexHandler),
    (r'/converter/?', ConverterHandler),
    (r'/wechat/?', WechatHandler),
    (r'/gencode/?', GenPayCodeHandler),
    (r'/download/?', DownloadHandler),
    
    (r"/(favicon\.ico)", StaticFileHandler, dict(path=settings.STATIC_PATH)),
]
