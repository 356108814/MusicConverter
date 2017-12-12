# encoding: utf-8
"""
视图模型基类
@author Yuriseus
@create 2016-8-4 19:56
"""

import json


class BaseViewModel(object):
    def __init__(self):
        self._model_dict = {}

    def update_by_json(self, json_content):
        try:
            data = json.loads(json_content)
        except Exception as e:
            data = None
        if data is not None:
            self.update_by_dict(data)

    def update_by_dict(self, data):
        fields = self.__dict__.keys()
        if isinstance(data, dict):
            for filed, v in data.items():
                if filed in fields:
                    setattr(self, filed, v)

    def process_dict(self, raw_dict):
        """
        dict数据处理，用来给子类实现
        @param raw_dict: 属性源数据
        @return:
        """
        pass

    def to_dict(self):
        attr_name = '_model_dict'    # 主要解决未经过__init__初始化的对象没有_model_dict的问题。如DBBaseModel
        if not hasattr(self, attr_name):
            self.__setattr__(attr_name, {})
        self._model_dict.update(self.__dict__)
        # 删除非自定义属性。注意：自定义对象属性不要以_开头
        keys = self._model_dict.keys()
        for key in list(keys):
            if key.startswith('_'):
                self._model_dict.pop(key)
        self._model_dict['__class__'] = self.__class__.__name__
        self.process_dict(self._model_dict)
        return self._model_dict


if __name__ == '__main__':
    s = json.loads('{"name":"test"}')
    print(s)
