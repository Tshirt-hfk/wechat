# -*- coding: utf-8 -*-
# filename: receive.py
import xml.etree.ElementTree as ET

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return RecvTextMsg(xmlData)
    elif msg_type == 'image':
        return RecvImageMsg(xmlData)
    elif msg_type == 'event':
        event_type = xmlData.find('Event').text
        if event_type == 'CLICK':
            return RecvClickEventMsg(xmlData)
        elif event_type in ('subscribe', 'unsubscribe'):
            return RecvEventMsg(xmlData)
        #elif event_type == 'VIEW':
            #return View(xmlData)
        #elif event_type == 'LOCATION':
            #return LocationEvent(xmlData)
        #elif event_type == 'SCAN':
            #return Scan(xmlData)
    else:
        return None

class RecvMsg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class RecvTextMsg(RecvMsg):
    def __init__(self, xmlData):
        RecvMsg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text

class RecvImageMsg(RecvMsg):
    def __init__(self, xmlData):
        RecvMsg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class RecvVoiceMsg(RecvMsg):
    def __init__(self, xmlData):
        RecvMsg.__init__(self, xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.Format = xmlData.find('Format').text

class RecvVedioMsg(RecvMsg):
    """收到的视频消息"""
    def __init__(self, xmlData):
        RecvMsg.__init__(self, xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.ThumbMediaId = xmlData.find('ThumbMediaId').text

class RecvShortvedioMsg(RecvMsg):
    """收到的小视频消息"""
    def __init__(self, xmlData):
        RecvMsg.__init__(self, xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.ThumbMediaId = xmlData.find('ThumbMediaId').text

class RecvLocationMsg(RecvMsg):
    """收到的位置消息"""
    def __init__(self, xmlData):
        RecvMsg.__init__(self, xmlData)
        self.Location_X = xmlData.find('Location_X').text
        self.Location_Y = xmlData.find('Location_Y').text
        self.Scale = xmlData.find('Scale').text
        self.Label = xmlData.find('Label').text

class RecvLinkMsg(RecvMsg):
    def __init__(self, xmlData):
        RecvMsg.__init__(self, xmlData)
        self.Title = xmlData.find('Title').text
        self.Description = xmlData.find('Description').text
        self.Url = xmlData.find('Url').text


# 事件消息

class RecvEventMsg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.Event = xmlData.find('Event').text
       
class RecvSubscribeEventMsg(RecvEventMsg):
    def __init__(self, xmlData):
        RecvEventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        self.Ticket = xmlData.find('Ticket').text

class RecvClickEventMsg(RecvEventMsg):
    def __init__(self, xmlData):
        RecvEventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text

class RecvViewEventMsg(RecvEventMsg):
    def __init__(self, xmlData):
        RecvEventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        

        
