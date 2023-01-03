from django.shortcuts import render

from django.http import HttpResponse, FileResponse

import os


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def restart(request):
    print("重启服务")
    os.system(r'../etc/openvpn/openvpn.run')
    return HttpResponse("服务重启成功！")

def download_config_file(request):
    print("下载配置文件")
    filepath=(r"OpenvpnManage\media\testfile.txt")
    return FileResponse(filepath)

def change_port(request):
    print("修改运行端口")
    print("重启服务")
    print("修改配置文件")
    return HttpResponse("端口修改成功！")

def start(request):
    print("启动服务")
    os.system(r'../etc/openvpn/openvpn.run')
    return HttpResponse("服务启动成功！")
