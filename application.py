# encoding: utf-8
"""
应用总配置
@author Yuriseus
@create 2016-8-1 14:12
"""
import configparser
import tornado.web
from tornado.util import import_object

import settings


class Application(tornado.web.Application):

    def __init__(self):

        # 加载配置
        self.load_conf()

        __settings = {
            'debug': settings.DEBUG,
            'static_path': settings.STATIC_PATH,
            'template_path': settings.TEMPLATE_PATH,
            'cookie_secret': 'LT4gKTS6nzTg'
        }
        from urls import handlers    # 不能放在顶部，需要等配置先加载完成，因为应用依赖配置
        super(Application, self).__init__(handlers=handlers, **__settings)

        # 初始化session管理
        from coffeebean.session import SessionManager
        self.session_manager = SessionManager()

        # 加载拦截器
        self.interceptor_intercept = None
        self.load_interceptor()

    def load_conf(self):
        parser = configparser.RawConfigParser()
        parser.read(settings.DEFAULT_CON_PATH, 'utf-8')
        sections = parser.sections()
        conf = settings.CONF
        for s in sections:
            if s not in conf:
                conf[s] = {}
            items = parser.items(s)
            for item in items:
                conf[s][item[0]] = item[1]

    def load_interceptor(self):
        self.interceptor_intercept = []
        for interceptor_path in settings.INTERCEPTOR_CLASSES:
            ic_class = import_object(interceptor_path)
            ic = ic_class()
            if hasattr(ic, 'intercept'):
                self.interceptor_intercept.append(ic.intercept)











