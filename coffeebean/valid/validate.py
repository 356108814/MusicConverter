# encoding: utf-8

"""
验证
@author Yuriseus
@create 2016-5-13 14:59
"""

from .validtype import *
from .config import RuleConfig


class Validate(object):
    def __init__(self):
        self._rules = {
            'regular': Regular(),
            'int': Int(),
            'number': Number(),
            'string': String(),
            'email': Email(),
            'mobile': Mobile(),
            'phone': Phone(),
            'url': Url(),
        }

    def is_valid(self, value, rule_config):
        """
        是否验证通过
        @param rule_config: 验证规则,RuleConfig
        @param value 待验证的值
        @return True验证通过，False验证失败
        """
        if not rule_config:
            return True
        if not rule_config.type:
            raise Exception(u'未配置验证类型type')
        rule_name = rule_config.type
        if rule_name not in self._rules:
            raise Exception(u'不支持的验证类型：%s' % rule_name)
        rule = self._rules[rule_name]
        rule.reset()
        return rule.is_valid(value, rule_config)

    def get_error_msg(self, rule_name):
        if rule_name not in self._rules:
            raise Exception(u'不支持的验证类型：%s' % rule_name)
        rule = self._rules[rule_name]
        return rule.error_msg


class ValidateParam(Validate):
    def __init__(self):
        super(ValidateParam, self).__init__()
        self._rule_config = RuleConfig()
        self._error_msg = ''

    def is_valid(self, value, config_dict):
        self._rule_config.reset()
        self._rule_config.update_by_dict(config_dict)
        return super(ValidateParam, self).is_valid(value, self._rule_config), self.get_error_msg(self._rule_config.type)


class ValidateForm(Validate):
    def __init__(self):
        super(ValidateForm, self).__init__()
        self._rule_config = RuleConfig()
        self._error_dict = {}

    def is_valid(self, param_dict, rule_config_dict):
        """
        是否为有效表单
        @param param_dict: 参数字典，包含名称和值，如django的POST，query_dict对象
        @param rule_config_dict: 规则配置。如：{'name': {}, 'password': {}}
        @return: True验证通过，False验证失败，错误信息dict
        """
        rtn_is_valid = True
        self._error_dict.clear()
        for name in rule_config_dict:
            value = None
            if name in param_dict:
                value = param_dict[name]
            rule_name = None
            if rule_config_dict and name in rule_config_dict:
                self._rule_config.reset()
                self._rule_config.update_by_dict(rule_config_dict[name])
                rule_name = self._rule_config.type
            if rule_name:
                is_valid = super(ValidateForm, self).is_valid(value, self._rule_config)
                if not is_valid:
                    rtn_is_valid = False
                    self._error_dict[name] = self.get_error_msg(rule_name)
        return rtn_is_valid, self._error_dict


if __name__ == '__main__':
    form = ValidateForm()





