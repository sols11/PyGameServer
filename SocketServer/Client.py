# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/12
Description:
	一个简单的用于测试的客户端，可模拟Unity Client
History:
----------------------------------------------------------------------------"""
import socket
import time
import struct
import json

client = socket.socket()
client.connect(("127.0.0.1", 8888))


# 我们设置包头为一个int数据，记录消息长度
def createHeadPack(size: int = 0):
	header = [size]
	headPack = struct.pack("!I", *header)
	return headPack


# 注册数据包（第一个参数为消息名）
def register(idStr, pwStr):
	body = json.dumps(dict(msg="Register", id=idStr, pw=pwStr))
	print(body)
	headPack = createHeadPack(len(body))
	return headPack + body.encode()


def login(idStr, pwStr):
	body = json.dumps(dict(msg="Login", id=idStr, pw=pwStr))
	headPack = createHeadPack(len(body))
	return headPack + body.encode()


def simpleCmd(cmd):
	body = json.dumps(dict(msg=cmd))
	print(body)
	headPack = createHeadPack(len(body))
	return headPack + body.encode()


# 正常数据包
client.send(register("Anotts", "86696686"))
# time.sleep(3)
# client.send(simpleCmd("Quit"))

# 接受消息
while True:
	data = client.recv(1024)
	# 将bytes转为str输出
	print("[收到信息]", data.decode())
	# msg = input("[发送信息]：")
	# client.send(simpleCmd(msg))
	# if msg == "Quit":
	# 	break
client.close()
