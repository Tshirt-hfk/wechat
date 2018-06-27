# -*- coding: utf-8 -*-
# filename: handle.py
from flask import Flask

from reply import *
from receive import *

from models import User

from datetime import date
import hashlib

app = Flask(__name__)

def signin(id):
	user = User.find(id)
	if not user:
		return '用户不存在，请重新关注'

	now = date.today()
	last = user.get('lastdate')
	day = (now - last).days

	if day == 0:
		return "当天已经签到过"
	elif day == 1:
		daynum = user.get("daynum")+1
		credit = user.get("credit")+5
		if daynum == 7:
			daynum = 0
			credit += 20
		u = User(id=user.get("id"), credit=credit, lastdate=now.strftime("%Y-%m-%d"), daynum=daynum)
		u.update()
		return "签到成功"
	elif day > 1:
		daynum = 1
		credit = user.get("credit")+5
		u = User(id=user.get("id"), credit=credit, lastdate=now.strftime("%Y-%m-%d"), daynum=daynum)
		u.update()
		return "签到成功"
	return "签到失败"

@app.route('/we', methods=['GET'])
def get():
	try:
		data = request.args
		if not data:
			return "hello, this is handle view"
		signature = data.get('signature')
		timestamp = data.get('timestamp')
		nonce = data.get('nonce')
		echostr = data.get('echostr')
		token = 'sao' #请按照公众平台官网\基本配置中信息填写
		list = [token, timestamp, nonce]
		list.sort()
		sha = hashlib.sha1()
		sha.update(''.join(list).encode('utf-8'))
		hashcode = sha.hexdigest()
		print("handle/GET func: hashcode, signature: ", hashcode, signature)
		if hashcode == signature:
			return echostr
		else:
			return ""
	except Exception as Argument:
		return Argument

@app.route('/we', methods=['POST'])
def post():
	try:
		webData = request.data.decode('utf-8')
		print("Handle Post webdata is\n", webData)   #后台打日志

		recvMsg = parse_xml(webData) # 解析收到的xml
		if recvMsg is None:
			return "success"

		if isinstance(recvMsg, RecvMsg):
			'''消息事件'''
			if recvMsg.MsgType == "text":
				toUser = recvMsg.FromUserName
				fromUser = recvMsg.ToUserName
				content = "test"
				replyMsg = ReplyTextMsg(toUser, fromUser, content)
				return replyMsg.send()
			else:
				print("暂不处理") 
				return "success"

		elif isinstance(recvMsg, RecvEventMsg):
			'''事件消息'''
			if recvMsg.Event == "CLICK":
				if recvMsg.Eventkey == "SIGNIN":
					'''签到事件'''
					title = signin(recvMsg.FromUserName)
					toUser = recvMsg.FromUserName
					fromUser = recvMsg.ToUserName
					replyMsg = ReplyNewsMsg(toUser, fromUser, title, "http://www.smbody.space/image/d4OEZKbGwauucho6DjvczkVAItGTkX.jpg")
					print('fuck')
					print(replyMsg.send())
					return replyMsg.send()
			elif recvMsg.Event == "subscribe":
				'''关注事件: 注册用户'''
				id = recvMsg.FromUserName
				u = User.find(id)
				if u == None:
					u = User(id=id, credit=0, lastdate=date(2000,1,1), daynum=0)
					u.save()
		else:
			print("暂不处理") 
			return "success"           
	except Exception as Argment:
		return Argment

@app.route('/we/image')
def get_code():
    #生成二维码图片
    image = Image.open('C:/1.jpg')
    image.thumbnail((360,250))
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    resp = Response(buffer, mimetype="image/jpeg")
    print(resp)
    return resp


