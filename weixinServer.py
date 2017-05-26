#coding:utf-8
import requests
import hashlib
from xml.etree import ElementTree as ET
from flask import Flask,request,make_response

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def wechat():
	# 微信通信验证
	if request.method == 'GET':
		signature = request.args.get('signature')
		timestamp = request.args.get('timestamp')
		nonce = request.args.get('echostr')
		token = 'yourToken'
		s = [timestamp,nonce,token]
		s.sort()
		s = ''.join(s).encode("utf-8")
		if(hashlib.sha1(s).hexdigest() == signature):
			return request.args.get('echostr')

	if request.method == 'POST':
		xml = ET.fromstring(request.stream.read())
		toUserName = xml.find('ToUserName').text
		fromUserName = xml.find('FromUserName').text
		createTime = xml.find('CreateTime').text
		msgType = xml.find('MsgType').text
		content = xml.find('Content').text
		if(msgType == 'text'):
			reply = '''
			    <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[%s]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
                ''' % (
                fromUserName,
               	toUserName,
               	createTime,
               	'text',
               	content
            )
			return reply
		else:
			return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)
