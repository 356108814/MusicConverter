# encoding: utf-8
"""
随机数
@author Yuriseus
@create 2016-8-4 20:00
"""
import random
import string


class RandomUtil(object):

    @staticmethod
    def random_string(num=10):
        """
        获取随机字符串
        @param num 长度
        """
        return ''.join(random.sample(string.digits + string.ascii_letters, num))

    @staticmethod
    def random_number(num=10):
        """
        获取随机数字字符串
        @param num 长度
        """
        return ''.join(random.sample(string.digits, num))