from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from xml.etree import ElementTree

import time

import hashlib

from urllib import request

import openai

import threading

from .wxGetToken import get_token_wx

import requests
import json


with open(r'key.key', 'r', encoding="UTF_8") as f:
    
    openai.api_key = f.readline()

def chat_gpt_mix(content):
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user", "content": content}
        ]
    )
    return completion.choices[0].message.content

def chat_gpt_dav(content):
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=content,
        max_tokens=1000,
        temperature=0.8
    )
    return completion.choices[0].text


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


class TransferCustomerService():
    def __init__(self, toUserName, fromUserName):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        # self.__dict['TransfeCustomerService'] = "transfer_customer_service"

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[transfer_customer_service]]></MsgType>
            </xml>
            """
        return XmlForm.format(**self.__dict)

 
def get_token(request):
    # 获取微信公众号token
    get_token_thread = threading.Thread(target=get_token_wx, args=("wxpublic.setting",))
    get_token_thread.start()
    return HttpResponse("获取token成功")


def reply_to_client(content, to_user):
    reply_content = chat_gpt_dav(content=content).strip()
    access_token = ""
    with open("wxToken.token", "r", encoding="UTF=8") as f:
        access_token = f.readline()
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}".format(access_token)
    data = {
        "touser":to_user,
        "msgtype":"text",
        "text":
        {
            "content": reply_content
        }
    }
    headers = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    print(reply_content)
    req = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(req.text)



def wx(request):
    # 用于处理微信服务器发来的请求
    if request.method == "GET":
        # 用于验证微信服务器
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
        # 用于处理请求
        web_data = request.body
        print(web_data)
        xml_data = ElementTree.fromstring(web_data)
        # 这里需要一个处理用户请求的函数
        msg_from_user = ParseXMLMsg(xml_data)
        # 转存用户请求  优先级往后排
        
        # 转存回答  优先级往后排
        
        # 定时功能，超出4.5s后先给用户返回消息 优先级往后排
        
        # 这里需要一个返回用户消息的函数
        # content = chat_gpt_dav(msg_from_user.Content).strip()
        # content = 'success'
        # send_msg = SendMsg(to_user, from_user, content)
        
        
        to_user = msg_from_user.FromUserName
        from_user = msg_from_user.ToUserName
        content = msg_from_user.Content
        reply_thread = threading.Thread(target=reply_to_client, args=(content, to_user))
        reply_thread.start()
        # 将客户消息转发至客服系统
        transfer_customer_service = TransferCustomerService(to_user, from_user).send()
        return HttpResponse(content=transfer_customer_service)
    

