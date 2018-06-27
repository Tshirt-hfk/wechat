# -*- coding: utf-8 -*-
# filename: menu.py
from urllib import request

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, str):
            postData = postData.encode('utf-8')
        urlResp = request.urlopen(url=postUrl, data=postData)
        print(urlResp.read())

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = request.urlopen(url=postUrl)
        print(urlResp.read())

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = request.urlopen(url=postUrl)
        print(urlResp.read())
        
    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = request.urlopen(url=postUrl)
        print(urlResp.read())

if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":[
        {  
            "type":"click",
            "name":"日签",
            "key":"SIGNIN"
        }]
    }
    """
    accessToken = Basic().get_access_token()
    print(accessToken)
    myMenu.create(postJson, accessToken)