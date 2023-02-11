# coding=utf-8
# 这是一个小小的里程碑，
# 因为我已经解决了关闭服务-更换端口-修改配置文件-重启服务的完整流程

from django.shortcuts import render

from django.core.files import File

from django.http import HttpResponse, FileResponse

from django.shortcuts import redirect

from django.template import loader

import os

import threading


# Create your views here.

def index(request):
    template = loader.get_template(r"OpenVPNApp/index.html")
    with open(r"setting.json", "r", encoding="UTF-8") as f:
        content = f.readlines()
        config_file = eval("".join(content))
    context = {
        "port": str(config_file["port"])
    }
    return HttpResponse(template.render(context, request))

def restart(request):
    print("重启服务")
    '''
    重启openvpn服务
    '''
    os.system(r'/etc/openvpn/killopenvpn.sh')
    start_openvpn_thread = threading.Thread(target=start_openvpn_fun)
    start_openvpn_thread.start()
    response = redirect("/openvpn/")
    return response
    # template = loader.get_template(r"OpenVPNApp/index.html")
    # with open(r"setting.json", "r", encoding="UTF-8") as f:
    #     content = f.readlines()
    #     config_file = eval("".join(content))
    # context = {
    #     "port": str(config_file["port"])
    # }
    # return HttpResponse(template.render(context, request))

def download_config_file(request):
    print("下载配置文件")
    filepath=(r"/home/OpenvpnManage/OpenVPNManage/media/client.ovpn")
    f = open(filepath, "rb")
    response = FileResponse(f)
    f.close
    response["content_type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment; filename=" + os.path.basename(filepath)
    return response

def start_openvpn_fun():
    # 运行linux重启服务的脚本
    os.system(r'/etc/openvpn/startopenvpn.sh')

def change_port(request):
    print("修改服务端配置文件的运行端口")
    create_server_config_file()
    print("重启服务")
    os.system(r'/etc/openvpn/killopenvpn.sh')
    start_openvpn_thread = threading.Thread(target=start_openvpn_fun)
    start_openvpn_thread.start()
    print("修改客户端配置文件")
    create_client_config_file()
    print("开启防火墙")
    response = redirect("/openvpn/")
    return response


config_file_content = []


import json

def create_client_config_file():
    
    config_file = {
    }

    with open(r"setting.json", "r", encoding="UTF-8") as f:
        content = f.readlines()
        config_file = eval("".join(content))
    with open(r"media/client-one.ovpn", "r", encoding="UTF-8") as f:
        config_file_content = f.readlines()
        config_file_content.append("remote " + config_file["ip"] + " " + str(config_file["port"]))
    with open(r"media/client.ovpn", "w", encoding="UTF-8") as f:
        f.write("".join(config_file_content))
    
def create_server_config_file(port=None):
    
    config_file = {
    }

    with open(r"setting.json", "r", encoding="UTF-8") as f:
        content = f.readlines()
        config_file = eval("".join(content))
        
    if port == None:
        config_file["port"] = config_file["port"] + 1
    else:
        config_file["port"] = port
        
    with open(r"media/server-one.conf", "r", encoding="UTF-8") as f:
        config_file_content = f.readlines()
        config_file_content.append("port "+ str(config_file["port"]))
    with open(r"/etc/openvpn/server_auto.conf", "w", encoding="UTF-8") as f:
        f.write("".join(config_file_content))
        
    with open(r"setting.json", "w", encoding="UTF-8") as f:
        f.write(json.dumps(config_file))
        
    os.system("ufw allow " + str(config_file["port"]))


if __name__ == "__main__":
    # 这是测试代码
    print("测试中")
    create_server_config_file()
    create_client_config_file()