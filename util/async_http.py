# encoding: utf-8
"""
异步http请求辅助类
@author Yuriseus
@create 2016-12-13 19:29
"""
import json
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError
from tornado.log import gen_log
from urllib.parse import urlencode


class AsyncHttpUtil(object):
    def __init__(self):
        pass

    def fetch(self, url, method=None, headers=None, body=None, callback=None):
        """
        执行请求
        :param url:
        :param method:
        :param headers:
        :param body:
        :param callback:  回调函数的值为HttpResponse
        :return:
        """
        http_client = AsyncHTTPClient()
        try:
            request = HTTPRequest(url, method=method, headers=headers, body=body)
            http_client.fetch(request, callback)
        except HTTPError as e:
            gen_log.warning("HttpHelper fetch Error: " + str(e))
        except Exception as e:
            gen_log("HttpHelper fetch Error: " + str(e))
        http_client.close()

    def get_data(self, url, headers=None, callback=None):
        self.fetch(url, method='GET', headers=headers, callback=callback)

    def post_data(self, url, headers=None, body=None, is_need_encode_body=False, callback=None):
        if is_need_encode_body:
                body = urlencode(body)
        else:
            if body is not None and not isinstance(body, str):
                body = str(body)
        self.fetch(url, method='POST', headers=headers, body=body, callback=callback)

    def to_json(self, content):
        try:
            if content:
                content = json.loads(content)
        except Exception as e:
            gen_log.warning("HttpHelper to json Error: " + str(e))
        return content

if __name__ == '__main__':
    pass
