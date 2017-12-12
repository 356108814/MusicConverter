# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-11 13:36
"""
import hashlib
import urllib
from urllib import parse
import settings

from coffeebean.log import logger
from models.message import Message
from service.manager import service_manger
from .base import BaseHandler

user_service = service_manger.user
converter_service = service_manger.converter
wechat_service = service_manger.wechat
pay_code_service = service_manger.pay_code


class WechatHandler(BaseHandler):
    
    def get(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        token = settings.CONF['wechat']['token']
        params = [token, timestamp, nonce]
        params.sort()
        sha1 = hashlib.sha1()
        sha1.update(''.join(params).encode('utf-8'))
        hashcode = sha1.hexdigest()
    
        if hashcode == signature:
            self.finish(echostr)
        else:
            self.finish("")
            
    def post(self):
        content = self.request.body
        logger.info(content)
        message = Message(content)
        # 初始化
        wechat_service.init_user(message.to_user_name, message.from_user_name)
        wechat_service.init_handler(self)
        if message.msg_type == 'event':
            if message.event == 'subscribe':
                user_service.insert_or_update(message.from_user_name)
                wechat_service.reply_text('真好呀，你没有错过我。这个地球上有几十亿人口，两个人相遇的概率只有千万分之一。\n\n'
                                          '歌曲下载，请直接回复链接即可。目前支持：咪哒、唱吧、友唱M-bar、全民K歌、哇屋wow。'
                                          '如有疑问或建议，直接加小扎微信，微信号：fhm911')
            return
        else:
            req_msg = message.content
            keywords = ['咪哒', '下载', '帮助', '歌曲', 'authorize', 'record/index.html', 'help']
            need_help = False
            for kw in keywords:
                if req_msg.find(kw) != -1:
                    need_help = True
                    break
            if need_help:
                wechat_service.reply_help()
                return
            
            if req_msg.startswith("keyc"):
                pay_code = pay_code_service.get(req_msg)
                if pay_code is None or pay_code['status'] == '1':
                    wechat_service.reply_text("无效的编码")
                    return
                else:
                    left_count = user_service.inc_count(message.from_user_name, pay_code['count'])
                    if left_count == -1:    # 找不到用户
                        wechat_service.reply_text("请先取消关注公众号，再重新关注，然后再回复密码")
                        return
                    pay_code_service.disable(req_msg)
                    wechat_service.reply_text("恭喜你，增加下载次数成功，剩余次数为：%s" % left_count)
                    return

            # 下载
            if req_msg.startswith("http"):
                if not user_service.is_can_download(message.from_user_name):
                    text = "由于下载带宽费用高昂，普通用户只能免费下载一首。如需继续下载，请加小扎微信赞助带宽费用，以红包形式，谢谢支持。赞助标准：2元一首，5首起步。小扎微信号：fhm911"
                    wechat_service.reply_text(text)
                else:
                    song = converter_service.convert(req_msg)
                    logger.info("converted song: %s" % song)
                    if song is not None:
                        user_service.reduce_count(message.from_user_name)
                        text = '注：苹果手机需要用电脑版微信下载\n\n<a href="{0}">{1}（点击直接下载）</a>'
                        song_url = urllib.parse.quote(song.url)
                        download_url = "http://converter.wezhake.com/download/?name={0}&url={1}".format(song.name, song_url)
                        text = text.format(download_url, song.name)
                        wechat_service.reply_text(text)
                    else:
                        wechat_service.reply_text("人工客服，请加小扎微信，微信号：fhm911")
            else:
                wechat_service.reply_text("人工客服，请加小扎微信，微信号：fhm911")

