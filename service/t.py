# encoding: utf-8
"""

@author Yuriseus
@create 2017-12-11 17:53
"""
import os
if __name__ == '__main__':
    
    a = os.path.splitext("http://wow-thunder.b0.upaiyun.com/record/201712/00E07E00A270_20171210122826_hG917k.mp3")
    f = "/details/19823140-&-788_LOW_20171105161805"
    array = f.replace("/details/", "").split("-&-")
    uid = array[0]
    jobid = array[1]
    print(uid)
    print(jobid)