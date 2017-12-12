# encoding: utf-8
"""
http请求辅助类
@author Yuriseus
@create 2016-8-4 19:29
"""
import json
from tornado import httpclient
from tornado.httpclient import HTTPRequest
from tornado.log import gen_log
from urllib.parse import urlencode


class HttpUtil(object):
    def __init__(self):
        pass

    def fetch(self, url, method=None, headers=None, body=None):
        content = ''
        http_client = httpclient.HTTPClient()
        try:
            request = HTTPRequest(url, method=method, headers=headers, body=body)
            response = http_client.fetch(request)
            content = response.body
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            gen_log.warning("HttpHelper fetch Error: " + str(e))
        except Exception as e:
            # Other errors are possible, such as IOError.
            gen_log("HttpHelper fetch Error: " + str(e))
        http_client.close()
        return content

    def get_data(self, url, headers=None):
        content = self.fetch(url, method='GET', headers=headers)
        return self.to_json(content)

    def post_data(self, url, headers=None, body=None, is_need_encode_body=False):
        if is_need_encode_body:
                body = urlencode(body)
        else:
            if body is not None and not isinstance(body, str):
                body = str(body)
        content = self.fetch(url, method='POST', headers=headers, body=body)
        return self.to_json(content)

    def to_json(self, content):
        try:
            if content:
                content = json.loads(content)
        except Exception as e:
            gen_log.warning("HttpHelper to json Error: " + str(e))
        return content

if __name__ == '__main__':
    pass
