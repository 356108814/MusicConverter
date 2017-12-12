# encoding: utf-8
"""
用户
@author Yuriseus
@create 2016-8-5 17:32
"""
# from .base import BaseService
from .base_mysql import BaseService


class UserService(BaseService):

    def __init__(self):
        super().__init__('user')

    def get(self, openid):
        sql = "SELECT * FROM " + self.table_name + " WHERE openid = %(openid)s"
        params_dict = {'openid': openid}
        return self.db.query(sql, params_dict, True)
    
    def insert_or_update(self, openid):
        user = self.get(openid)
        if user is None:
            info = {'openid': openid, 'nickname': '', 'headimgurl': '', 'count': 0, 'is_pay': 0}
            self.save(info)
    
    def inc_count(self, openid, count):
        user = self.get(openid)
        self.logger.info("user:" + str(user))
        if user:
            new_count = user['count'] + count
            self.update_count(openid, new_count)
            return new_count
        return -1
    
    def reduce_count(self, openid, count=1):
        user = self.get(openid)
        new_count = user['count'] - count
        return self.update_count(openid, new_count)
    
    def update_count(self, openid, count):
        sql = "UPDATE " + self.table_name + " SET count = %(count)s WHERE openid = %(openid)s"
        params_dict = {'openid': openid, 'count': count}
        return self.db.execute(sql, params_dict)
    
    def is_can_download(self, openid):
        user = self.get(openid)
        return user is not None and user['count'] > 0
        



