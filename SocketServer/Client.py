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
from Core import System

client = socket.socket()
client.connect(("127.0.0.1", 8888))


# 注册数据包（第一个参数为消息名）
def register(idStr, pwStr):
	body = json.dumps(dict(id=idStr, pw=pwStr))
	return System.CreatePackage("Register", body)


def login(idStr, pwStr):
	body = json.dumps(dict(id=idStr, pw=pwStr))
	return System.CreatePackage("Login", body)


def simpleCmd(cmd: str):
	return System.CreatePackage(cmd)


# 正常数据包
client.send(register("Anotts", "86696686"))
# client.send(register("测试用户", "123321"))
# time.sleep(3)
# client.send(simpleCmd("Quit"))

# 接受消息
while True:
	data = client.recv(1024)
	# 将bytes转为str输出
	if data:
		print("[收到信息]", data.decode())
	# msg = input("[发送信息]：")
	# client.send(simpleCmd(msg))
	# if msg == "Quit":
	# 	break
client.close()
