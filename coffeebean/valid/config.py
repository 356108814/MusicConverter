# encoding: utf-8
"""
单个字段的验证配置，对应配置格式：{'type': 'int', 'required':True, 'min': 0, 'max': 100}
@author Yuriseus
@create 2016-5-15 8:35
"""


class RuleConfig(object):
    def __init__(self):
        self.type = None    # 验证类型
        self.required = None
        self.min = None
        self.max = None

    def reset(self):
        self.__init__()

    def update_by_dict(self, data):
        fields = self.__dict__.keys()
        if isinstance(data, dict):
            for field in data:
                if field in fields:
                    if field in ['min', 'max']:
                        field_value = int(data[field])
                    else:
                        field_value = data[field]
                    setattr(self, field, field_value)

if __name__ == '__main__':
    c = RuleConfig()
    # c['a'] = 1
    print(c.type)
