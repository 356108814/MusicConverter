# encoding: utf-8
import os
import urllib
from tornado.web import RequestHandler
from urllib import parse
from urllib import request


class DownloadHandler(RequestHandler):
    def get(self):
        name = self.get_argument("name")
        url = self.get_argument("url")
        ext = os.path.splitext(url)[1]
        # 中文名附件必须quote
        filename = urllib.parse.quote(name + ext)
        self.set_header('Content-Type', 'application/octet-stream;')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
        f = request.urlopen(url)
        self.write(f.read())
        self.finish()
