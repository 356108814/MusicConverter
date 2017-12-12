# encoding: utf-8
"""
验证拦截器
@author Yuriseus
@create 2016-8-3 16:46
"""
from coffeebean.interceptor.interface import Interceptor


class AuthInterceptor(Interceptor):
    def intercept(self, handler):
        path = handler.request.path
        # if path not in ['/login/', '/login']:
        #     user = handler.session['user']
        #     if not user:
        #         handler.redirect('/login')
        #     return True
        return True

