from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from xml.etree import ElementTree

import time

import hashlib


import openai

openai.api_key = "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"


def chat_gpt_mix(content):
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"user", "content": content}
    ]
    )
    return completion.choices[0].message.content

class ParseXMLMsg():
    def __init__(self, xml_msg):
        self.ToUserName = xml_msg.find('ToUserName').text
        self.FromUserName = xml_msg.find('FromUserName').text
        self.CreateTime = xml_msg.find('CreateTime').text
        self.MsgType = xml_msg.find('MsgType').text
        self.MsgId = xml_msg.find('MsgId').text
        self.Content = xml_msg.find('Content').text
        # self.ToUserName = xml_msg.find('ToUserName')
        # self.FromUserName = xml_msg.find('FromUserName')
        # self.CreateTime = xml_msg.find('CreateTime')
        # self.MsgType = xml_msg.find('MsgType')
        # self.MsgId = xml_msg.find('MsgId')
        # self.Content = xml_msg.find('Content').encode('UTF-8')

class SendMsg():
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
        return XmlForm.format(**self.__dict)

def wx(request):
    # 用于验证微信服务器
    if request.method == "GET":
        signature = request.GET.get('signature')
        echostr = request.GET.get('echostr')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        token = 'zzq'
        list = [nonce, token, timestamp]
        list.sort()
        liststr = "".join(list).encode("UTF-8")
        sha1 = hashlib.sha1()
        sha1.update(liststr)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return HttpResponse(content=echostr)
        else:
            return HttpResponse(content="验证失败")
    elif request.method == "POST":
        web_data = request.body
        print(web_data)
        xml_data = ElementTree.fromstring(web_data)
        # 这里需要一个处理用户请求的函数
        msg_from_user = ParseXMLMsg(xml_data)
        # 转存用户请求  优先级往后排
        
        # 转存回答  优先级往后排
        
        # 定时功能，超出4.5s后先给用户返回消息 优先级往后排
        
        # 这里需要一个返回用户消息的函数
        to_user = msg_from_user.FromUserName
        from_user = msg_from_user.ToUserName
        content = chat_gpt_mix(msg_from_user.Content)[2:]
        send_msg = SendMsg(to_user, from_user, content)
        return HttpResponse(content=send_msg.send())
    