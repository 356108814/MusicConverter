# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-10 10:57
"""


class Song(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url
        
    def __str__(self):
        return "name:{0}，url:{1}".format(self.name, self.url)
