# encoding: utf-8
"""
首页
@author Yuriseus
@create 2016-8-1 18:09
"""
from .base import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")
