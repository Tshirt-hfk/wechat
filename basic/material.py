# -*- coding: utf-8 -*-
# filename: material
from basic import Basic
import requests

appId = 'wxb3679ac24461d7bc'
appSecret = '0a3e5c2826926e3e1e750cf0ee797f98'

class Material(object):
	"""素材管理类"""
	def __init__(self):
		self.__basic = Basic(appId, appSecret)
		# self.__basic.start()

	def uploadMaterial(self, types, file):
		print(self.__basic.get_access_token())
		postUrl = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s' % (self.__basic.get_access_token(), types)
		print(postUrl)
		files = {
			'media': ('1.jpg', file, 'image/jpg')
		}
		req = requests.post(url=postUrl, files=files)
		print(req.text)

m = Material()
f = open("E:1.jpg",'rb')
print(type(f))
m.uploadMaterial(types='image', file=f)