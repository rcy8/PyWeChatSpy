from PyWeChatSpy import WeChatSpy
from PyWeChatSpy.command import *
from lxml import etree
import requests
import time
import logging
from PyWeChatSpy.proto import spy_pb2
import base64
import os
from queue import Queue


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
logger.addHandler(sh)


groups = []
WECHAT_PROFILE = r"D:\Documents\WeChat Files"
my_response_queue = Queue()


def handle_response():
    while True:
        data = my_response_queue.get()
        f=open(r"C:\test\dist\微信.txt",'a')
        f.write(str(data))
        f.write('\n')
        #print(data)
        if data.type == PROFESSIONAL_KEY:
            if not data.code:
                logger.error(data.message)
        elif data.type == WECHAT_CONNECTED:  # 微信接入
            print(f"微信客户端已接入 port:{data.port}")
        elif data.type == HEART_BEAT:  # 通过获取心跳数据来实现推送！！！
            ts2 = time.strftime("%H:%M:%S", time.localtime())
            print(ts2)
            if ts2 >='18:09:00' and ts2<'18:09:05':
                spy.send_text("gh_bf214c93111c", "#4936 sc")
            elif ts2 >= '18:10:00' and ts2 < '18:10:05':
                spy.send_file("gh_bf214c93111c", r"C:\test\dist\ma北向净流入.png")
            pass
        elif data.type == WECHAT_LOGIN:  # 微信登录
            a=spy.get_account_details()  # 获取登录账号详情
            print(a)
            # ts2 = time.strftime("%H:%M", time.localtime())
            # if ts2 =='14:57':
            #     spy.send_text("gh_bf214c93111c","#4936 sc")wxid_ngkfoaf6cyqs21
            pass
        elif data.type == WECHAT_LOGOUT:  # 微信登出
            pass
        elif data.type == CHAT_MESSAGE:  # 微信消息
            chat_message = spy_pb2.ChatMessage()
            print(chat_message)
            chat_message.ParseFromString(data.bytes)
            for message in chat_message.message:
                _type = message.type  # 消息类型 1.文本|3.图片...自行探索
                _from = message.wxidFrom.str  # 消息发送方
                _to = message.wxidTo.str  # 消息接收方
                content = message.content.str  # 消息内容
                if _from=='wxid_84vpsbomtynb32':
                    url='http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s'%content
                    r = requests.get(url)
                    cont = r.json()
                    c = cont['content']
                    spy.send_text("wxid_84vpsbomtynb32",c)
                else:
                    image_overview_size = message.imageOverview.imageSize  # 图片缩略图大小
                    image_overview_bytes = message.imageOverview.imageBytes  # 图片缩略图数据
                    with open(r"C:\npy\wc\im\img.jpg", "wb") as wf:
                        wf.write(image_overview_bytes)
                    overview = message.overview  # 消息缩略
                    timestamp = message.timestamp  # 消息时间戳
                    print(timestamp,overview)
                    if _type == 1:  # 文本消息
                        print(_from, _to, content)
                        if _to == "filehelper":
                            spy.send_text("filehelper", "Hello PyWeChatSpy3.0\n" + content)
                    elif _type == 3:  # 图片消息
                        file_path = message.file
                        print(_from, _to, content, file_path)
                        file_path = os.path.join(WECHAT_PROFILE, file_path)
                        time.sleep(10)
                        #ts = time.strftime("%Y/%m/%d %H:%M", time.localtime())
                        spy.decrypt_image(file_path, r"C:\npy\wc\im\a.jpg")
                    elif _type == 43:  # 视频消息
                        print(_from, _to, content, message.file)
                    elif _type == 49:  # XML报文消息
                        print(_from, content, message.file)
                    elif _type == 37:  # 好友申请
                        print(message.content)
                        obj = etree.XML(message.content.str)
                        encryptusername, ticket = obj.xpath("/msg/@encryptusername")[0], obj.xpath("/msg/@ticket")[0]
                        spy.accept_new_contact(encryptusername, ticket)  # 接收好友请求


if __name__ == '__main__':
    spy = WeChatSpy(response_queue=my_response_queue, key="18d421169d93611a5584affac335e690", logger=logger)
    pid = spy.run(r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe")
    handle_response()


