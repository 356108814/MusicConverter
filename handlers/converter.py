# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-10 15:05
"""
from service.manager import service_manger
from .base import BaseHandler

converter = service_manger.converter


class ConverterHandler(BaseHandler):
    
    def get(self):
        url = self.get_argument("url", "")
        song = self.get_song(url)
        self.write_response(song)
    
    def post(self):
        url = self.request.body.decode()
        song = self.get_song(url)
        self.write_response(song)
    
    def get_song(self, url):
        song = None
        if url != "":
            song = converter.convert(url)
        return song
