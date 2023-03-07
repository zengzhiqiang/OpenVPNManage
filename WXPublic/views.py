from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import hashlib


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
        pass