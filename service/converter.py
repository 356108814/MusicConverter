# encoding: utf-8
"""
歌曲转换器
@author Yuriseus
@create 2017-12-10 10:06
"""
import json
import re
import subprocess
from bs4 import BeautifulSoup
from urllib import parse
from urllib import request

from coffeebean.log import logger
from models.song import Song


class Converter(object):
    
    def __init__(self):
        pass
    
    def convert(self, url):
        song = None
        try:
            if url.startswith("http://weixin.singworld.cn/"):
                song = self.minik(url)
            elif url.startswith("http://changba.com"):
                song = self.changba(url)
            elif url.find("qq.com") != -1 or url.find("kg.qq.com") != -1 or url.find("kg2.qq.com") != -1:
                song = self.quan_min(url)
            elif url.find("uc.ipktv.com") != -1:
                song = self.youchang(url)
            elif url.find("vod.ktvsky.com") != -1:
                song = self.wow(url)
            elif url.startswith("http://www.quanminktv.cn"):
                song = self.quanmin_ktv(url)
        except Exception as e:
            logger.error(e)

        return song
    
    def minik(self, url):
        # 解析参数
        result = parse.urlparse(url)
        params = parse.parse_qs(result.query)
        if "uid" in params and 'jobid' in params:
            uid = params['uid'][0]
            jobid = params['jobid'][0]
        else:
            fragment = str(result.fragment)
            if fragment.find("-&-") != -1:
                array = fragment.replace("/details/", "").split("-&-")
                uid = array[0]
                jobid = array[1]
            else:
                jobid = fragment.replace("/details/", "").replace("--ml--", "")
                params = parse.parse_qs(result.query)
                uid = params['uid'][0]

        req_url = "http://weixin.singworld.cn/api/record/record_detail/?&uid={0}&jobid={1}".format(uid, jobid)
        content = Converter.get_content(req_url)
        music_info = json.loads(content)['data']['record']
        song_url = "http://{0}/{1}".format(music_info['domain'], music_info['url'])
        song = Song(music_info['song_name'], song_url)
        return song

    def minik2(self, uid, jobid):
        # 解析参数
        req_url = "http://weixin.singworld.cn/api/record/record_detail/?&uid={0}&jobid={1}".format(uid, jobid)
        content = Converter.get_content(req_url)
        music_info = json.loads(content)['data']['record']
        song_url = "http://{0}/{1}".format(music_info['domain'], music_info['url'])
        song = Song(music_info['song_name'], song_url)
        return song

    def changba(self, url):
        content = Converter.get_content(url)
        # <div class="title">普通的disco【洛天依】</div>
        # (function(){var a="http://qiniuuwmp3.changba.com/939278470.mp3"
        name_matches = re.findall(r'<div class="title">(.*)</div>', content, re.M)
        url_matches = re.findall(r'http:.*\.mp3",', content, re.M)
        song_name = name_matches[0].replace("\",", "")
        song_url = url_matches[0].replace("\",", "")
        song = Song(song_name, song_url)
        return song
    
    def quan_min(self, url):
        content = Converter.get_content(url)
        bs = BeautifulSoup(content, 'html.parser')
        elements = bs.find_all('script', type='text/javascript')
        song = None
        for element in elements:
            if element is not None and str(element.string).startswith("window.__DATA__"):
                info = str(element.string).replace("window.__DATA__ =", "").replace(";", "")
                music_info = json.loads(info)["detail"]
                song = Song(music_info["song_name"], music_info["playurl"])
                break
        return song
    
    def wow(self, url):
        api = "http://localhost:8050/render.html?url={0}&timeout=10&wait=0.5".format(url)
        logger.info("wow url: %s" % api)
        # content = self.get_content(api)
        content = subprocess.getoutput("curl %s" % api)
        # class="name">盛夏的果实</p>
        # id="audio" src="http://wow-thunder.b0.upaiyun.com/record/201712/00E07E00A270_20171208185730_fmliMb.mp3" preload="metadata"></audio>
        name_matches = re.findall(r'class="name">(.*)</p>', content, re.M)
        url_matches = re.findall(r'http://wow-thunder.*\.mp3', content, re.M)
        song_name = name_matches[0]
        song_url = url_matches[0]
        song = Song(song_name, song_url)
        return song
    
    def youchang(self, url):
        result = parse.urlparse(url)
        if url.find("shareDetail") != -1:
            fragment = result.fragment
            index = str(fragment).replace("/shareDetail/", "")
        elif url.find("?id="):
            index = str(result.query).replace("id=", "")
        
        api_url = "https://uc.ipktv.com/youCS/youC20170216/wxYouCApi20170330/index"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400"}
        values = {"header": {"data_type": "proxy", "data_direction": "request", "server": "vod_http_server",
                             "id": "vod_http_server"},
                  "request": {"function": 10207, "version": "1.0", "clientFunc": "dataQuery",
                              "privateFunc": "immediateIndex", "fondDebug": "", "id": "{0}".format(index),
                              "user_id": "113081042",
                              "url": "https://uc.ipktv.com/youCS/youC20170216/youCShare/index#/shareDetail/" + index},
                  "comment": ""}
        req = request.Request(api_url, headers=headers, method="POST")
        response = request.urlopen(req, json.dumps(values).encode())
        json_obj = json.loads(response.read().decode())
        print(json_obj)
        music_info = json_obj['response']['data']['row']
        
        song = Song(music_info['_title'], music_info['_merge_songs_file_url_mp3'])
        return song

    def quanmin_ktv(self, url):
        api = "http://localhost:8050/render.html?url={0}&timeout=10&wait=0.5".format(url)
        content = subprocess.getoutput("curl %s" % api)
        bs = BeautifulSoup(content, 'html.parser')
        song_url = bs.find('video').attrs['src']
        song_name = bs.find("h3", {"id": "song_name"}).text
        song = Song(song_name, song_url)
        return song
    
    @staticmethod
    def get_content(url, encoding="utf-8"):
        f = request.urlopen(url)
        return f.read().decode(encoding)


if __name__ == '__main__':
    req_url = "https://kg.qq.com/node/play?s=tGE9XrtqVcWTKtms"
    req_url = "http://changba.com/s/dfmUU7cLNlynZAG5hQrXsQ?&code=RkvQSz26klqSrOkSuFVHIacdpsUjbX4zL9c2vg82dbU3L_I2RK_eDEuCrjBzuklN-ci288TsX1ONcqXOXW0U5TJ7U0J8Bi32QrXF6D9NxfE"
    req_url = "https://vod.ktvsky.com/dp/song?id=10289542"
    req_url = "http://weixin.singworld.cn/web_frontend_alipay/share_cp/?songid=C007600&uid=21249984&uuid=4db34f4e-52cc-4a6e-b6c5-2e6068267d66&zfflag=0#/details/57775_LOW_20171208202751--ml--"
    req_url = "https://uc.ipktv.com/youCS/youC20170216/youCShare/index#/shareDetail/54217849?play=0"
    req_url = "http://weixin.singworld.cn/web_frontend/share_cp/?share=1&uid=6692089&uuid=1ea03a3e-16ae-4d17-83cb-1f2923cd749c#/details/3284_20170602170056--ml--"
    req_url = "http://www.quanminktv.cn/wechat/videoPlay?video_id=1103&owner_openid=oZkxjv-Qx3MulS6IxAmPilPVzFIQ"
    req_url = "http://uservideos.oss-cn-beijing.aliyuncs.com/2C14E81539814F8D8ECCE11D826E7002"
    req_url = "http://uc.ipktv.com/youCS/youC20170216/youCShare/index?from=singlemessage#/shareDetail/64566091"
    req_url = "https://kg2.qq.com/node/play?s=gM-W8wgVE7X2Cgog&shareuid=679e9483262c3583&topsource=&from=singlemessage&isappinstalled=0"
    req_url = "http://uc.ipktv.com/youCS/youC20170216/youCShare/index#/shareDetail/14393247"
    req_url = "http://weixin.singworld.cn/web_frontend_alipay/record/?zf_flag=0#/photos/16276112-&-49030_LOW_20180105161000"
    req_url = "http://uc.ipktv.com/youCS/youC20170216/youCShare/index?id=76405366"
    req_url = "http://weixin.singworld.cn/web_frontend/gift/?bag_id=89001&uid=24693743&activity_id=180220019&jobid=3784_LOW_20180209165618&zf_flag=0#/show/"
    converter = Converter()
    print(converter.convert(req_url))
