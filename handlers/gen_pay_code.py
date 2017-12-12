# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-11 13:36
"""

from service.manager import service_manger
from .base import BaseHandler

pay_code_service = service_manger.pay_code


class GenPayCodeHandler(BaseHandler):
    
    def get(self):
        count = int(self.get_argument("count"))
        code = pay_code_service.gen(count)
        self.finish(code)




