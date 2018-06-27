# -*- coding: utf-8 -*-
# filename: reply.py
import time

class ReplyMsg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class ReplyTextMsg(ReplyMsg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        print(XmlForm.format(**self.__dict))
        return XmlForm.format(**self.__dict)
    
class ReplyImageMsg(ReplyMsg):
    def __init__(self, toUserName, fromUserName, mdeiaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mdeiaId

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <Media><![CDATA[{Media}]]></Media>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)

class ReplyNewsMsg(ReplyMsg):
    def __init__(self, toUserName, fromUserName, title, picUrl):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Title'] = title
        self.__dict['PicUrl'] = picUrl

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[{Title}]]></Title>
        <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
        </item>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)
        
