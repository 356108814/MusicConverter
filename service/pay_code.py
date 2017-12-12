# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-11 14:52
"""
import time
from .base_mysql import BaseService


class PayCodeService(BaseService):
    
    def __init__(self):
        super().__init__('paycode')
        
    def gen(self, count):
        code = 'keyc' + str(int(time.time()))
        info = {'code': code, 'type': 'a', 'count': count, 'status': '0'}
        success = self.save(info)
        if success:
            return code
        return ""

    def get(self, code):
        sql = "SELECT * FROM " + self.table_name + " WHERE code = %(code)s"
        return self.db.query(sql, {'code': code}, True)
    
    def disable(self, code):
        sql = "UPDATE " + self.table_name + " SET status = '1' WHERE code = %(code)s"
        params_dict = {'code': code}
        return self.db.execute(sql, params_dict)
