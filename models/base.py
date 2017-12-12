# encoding: utf-8
"""
模型基类
@author Yuriseus
@create 2016-12-10 21:09
"""


class BaseModel(object):

    def to_dict(self):
        return self.__dict__

    def update_by_dict(self, data):
        fields = self.__dict__.keys()
        if isinstance(data, dict):
            for filed, v in data.items():
                if filed in fields:
                    setattr(self, filed, v)
