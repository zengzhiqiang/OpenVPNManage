import urllib.request as rq
import time
import json
import threading

AppID = ""
AppSecret = ""



def get_token_wx(path):
    with open(path, "r", encoding="UTF-8") as f:
    # 获取设定
        settings = f.readlines()
        AppID = settings[0].strip()
        AppSecret = settings[1].strip()
    url_base = "https://api.weixin.qq.com/cgi-bin/token?grant_type={0}&appid={1}&secret={2}".format("client_credential", AppID, AppSecret)
    while True:
        wx_token_data_response = rq.urlopen(url=url_base)
        wx_token_data = wx_token_data_response.read().decode("UTF-8")
        wx_token = json.loads(wx_token_data)
        try:
            access_token = wx_token["access_token"]
            with open("wxToken.token", "w", encoding="UTF-8") as f:

                f.write(access_token)
        except:
            print("access_token获取失败，微信服务器回复如下！")
            print(wx_token)
        # print(wx_token_data)
        time.sleep(7000)
    # client_credential

if __name__ == "__main__":
    # get_token_wx()
    get_wx_token_threading = threading.Thread(target=get_token_wx, args=(r"OpenvpnManage\wxpublic.setting",))
    get_wx_token_threading.start()
    
