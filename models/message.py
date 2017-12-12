# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-11 14:22
"""
from xml.etree import ElementTree as ET


class Message(object):
    def __init__(self, xml):
        self.xml = xml
        self.root = ET.fromstring(xml)
        self.to_user_name = self.root.find('ToUserName').text
        self.from_user_name = self.root.find('FromUserName').text
        self.create_time = self.root.find('CreateTime').text
        self.msg_type = self.root.find('MsgType').text

    @property
    def content(self):
        return self.root.find('Content').text
    
    @property
    def event_key(self):
        return self.root.find('EventKey').text

    @property
    def event(self):
        return self.root.find('Event').text
    
    
if __name__ == '__main__':
    s = """<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>"""
    message = Message(s)
    print(message.from_user_name)
    print(message)
