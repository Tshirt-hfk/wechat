# -*- coding: utf-8 -*-
# filename: basic.py
import time, json
from urllib import request
from threading import Thread

class Basic(Thread):
    def __init__(self, appId, appSecret):
        Thread.__init__(self)
        self.__accessToken = ''
        self.__leftTime = 0
        self.__postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
    def __real_get_access_token(self):
        print(self.__postUrl)
        urlResp = request.urlopen(self.__postUrl).read().decode('utf-8')
        urlResp = json.loads(urlResp)
        
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']     

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()