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

client = socket.socket()
client.connect(("127.0.0.1", 8888))

while True:
	data = client.recv(1024)
	# 将bytes转为str输出
	print("[收到信息]", data.decode())
	msg = input("[发送信息]：")
	client.send(msg.encode())
	if msg == "quit":
		break
