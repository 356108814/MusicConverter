# encoding: utf-8

"""
验证类型
@author Yuriseus
@create 2016-5-13 14:59
"""

import re


class Regular(object):
    """自定义正则验证基类"""
    def __init__(self, pattern='', error_msg=u'格式不正确', name=None):
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__.lower()
        self.pattern = pattern
        self.rule_config = None
        self.error_msg = error_msg

    def is_valid(self, value, rule_config=None):
        """
        是否验证通过。模板方法
        @param value 值
        @param rule_config 规则配置，对应RuleConfig
        @return True验证通过，False验证失败
        """
        self.rule_config = rule_config
        if not self.rule_config.required and not value:    # 非必须参数，而且未传值，直接返回True
            return True
        is_valid = self.valid_required(value)
        if is_valid:
            is_valid = self.valid_pattern(value)
            if is_valid:
                is_valid = self.valid_range(value)
        return is_valid

    def valid_required(self, value):
        if self.rule_config.required and not value:
            self.error_msg = u'为必选项，不能为空'
            return False
        return True

    def valid_pattern(self, value):
        is_match = re.compile(self.pattern).match(str(value)) is not None
        if not is_match:
            # self.error_msg = u'为必选项，不能为空'
            pass
        return is_match

    def valid_range(self, value):
        """验证数值范围"""
        value = int(value)
        min_value = self.rule_config.min
        max_value = self.rule_config.max
        if min_value is None and min_value is None:
            return True
        if min_value is not None and max_value is None:
            if value < min_value:
                self.error_msg = u'值必须大于等于%s' % str(min_value)
                return False
        elif min_value is None and min_value is not None:
            if value > max_value:
                self.error_msg = u'值必须小于等于：%s' % str(max_value)
                return False
        elif not (min_value <= value <= max_value):
            self.error_msg = u'值必须介于%s和%s之间' % (str(min_value), str(max_value))
            return False
        return True

    def reset(self):
        pass


class Int(Regular):
    """整数"""
    def __init__(self):
        super(Int, self).__init__('^[-]?[0-9]+$')
        self.reset()

    def reset(self):
        self.error_msg = u'只能输入整数'


class Number(Regular):
    """数字"""
    def __init__(self):
        super(Number, self).__init__('^[-]?[0-9]+[.]?[0-9]+$')

    def reset(self):
        self.error_msg = u'只能输入数字'


class String(Regular):
    """指定长度字符串"""
    def __init__(self):
        super(String, self).__init__('')

    def valid_range(self, value):
        length = 0
        if value:
            length = len(value)
        return super(String, self).valid_range(length)

    def reset(self):
        self.error_msg = u'字符串长度必须介于{0}到{1}之间'


class Email(Regular):
    """邮箱"""
    def __init__(self):
        super(Email, self).__init__('^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]+$')

    def reset(self):
        self.error_msg = u'邮箱格式不正确'


class Mobile(Regular):
    """手机号"""
    def __init__(self):
        super(Mobile, self).__init__('^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|171|18[0|1|2|3|5|6|7|8|9])\d{8}$')

    def reset(self):
        self.error_msg = u'手机号格式不正确'


class Phone(Regular):
    """电话号码"""
    def __init__(self):
        super(Phone, self).__init__('^\d{3}[-]?\d{8}|\d{4}[-]?\d{7}$')

    def reset(self):
        self.error_msg = u'电话号码格式不正确'


class Url(Regular):
    """网址"""
    def __init__(self):
        super(Url, self).__init__('^(\w+:\/\/)?\w+(\.\w+)+.*$')

    def valid_range(self, value):
        return super(Url, self).valid_range(len(value))

    def reset(self):
        self.error_msg = u'url格式不正确'



