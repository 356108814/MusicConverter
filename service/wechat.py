# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-11 14:15
"""
import time
from coffeebean.log import logger


class WechatService(object):
    
    def __init__(self):
        self.from_user = ""
        self.to_user = ""
        self.handler = None
    
    def init_user(self, from_user, to_user):
        self.from_user = from_user
        self.to_user = to_user

    def init_handler(self, handler):
        self.handler = handler
    
    def reply_text(self, msg):
        tpl = """<xml>
<ToUserName><![CDATA[{0}]]></ToUserName>
<FromUserName><![CDATA[{1}]]></FromUserName>
<CreateTime>{2}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{3}]]></Content>
</xml>"""
        text = tpl.format(self.to_user, self.from_user, int(time.time()), msg)
        self.handler.finish(text)
        return text
    
    def reply_news(self, title, desc, pic_url, url):
        tpl = """<xml>
<ToUserName><![CDATA[{0}]]></ToUserName>
<FromUserName><![CDATA[{1}]]></FromUserName>
<CreateTime>{2}</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
<Title><![CDATA[{3}]]></Title>
<Description><![CDATA[{4}]]></Description>
<PicUrl><![CDATA[{5}]]></PicUrl>
<Url><![CDATA[{6}]]></Url>
</item>
</Articles>
</xml>"""
        text = tpl.format(self.from_user, self.to_user, int(time.time()), title, desc, pic_url, url)
        self.handler.finish(text)
        return text
    
    def reply_help(self):
        title = "如何下载咪哒歌曲"
        desc = "简单分2步，复制歌曲链接，发送链接到公众号"
        pic_url = "http://www.wezhake.com/static/images/helpNews.jpg"
        url = "https://mp.weixin.qq.com/s?__biz=MzA3MDc4ODUzNg==&mid=2449538103&idx=1&sn=ab6c58379a822e7e9bfd8534277951d0&chksm=88c328e0bfb4a1f6ede83aaa34688017979281959ee4eda853231c3bfbdbc2ed8a213c1bee79#rd"
        return self.reply_news(title, desc, pic_url, url)
