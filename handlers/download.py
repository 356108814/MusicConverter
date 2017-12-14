# encoding: utf-8
import os
import urllib
from tornado.web import RequestHandler
from urllib import parse
from urllib import request


class DownloadHandler(RequestHandler):
    def get(self):
        name = self.get_argument("name")
        url = str(self.get_argument("url"))
        ext = os.path.splitext(url)[1]
        if url.find("aliyuncs") != -1:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400"}
            ext = ".mp4"
        else:
            headers = {}
        # 中文名附件必须quote
        filename = urllib.parse.quote(name + ext)
        self.set_header('Content-Type', 'application/octet-stream;')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
        
        req = request.Request(url, headers=headers)
        f = request.urlopen(req)
        self.write(f.read())
        self.finish()
