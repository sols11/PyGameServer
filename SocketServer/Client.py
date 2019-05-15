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

# 正常数据包定义
ver = 1
body = json.dumps(dict(hello="world"))
print(body)
cmd = 101
header = [ver, body.__len__(), cmd]
headPack = struct.pack("!3I", *header)
sendData1 = headPack + body.encode()

# 分包数据定义
ver = 2
body = json.dumps(dict(hello="world2"))
print(body)
cmd = 102
header = [ver, body.__len__(), cmd]
headPack = struct.pack("!3I", *header)
sendData2_1 = headPack + body[:2].encode()
sendData2_2 = body[2:].encode()

# 粘包数据定义
ver = 3
body1 = json.dumps(dict(hello="world3"))
print(body1)
cmd = 103
header = [ver, body1.__len__(), cmd]
headPack1 = struct.pack("!3I", *header)

ver = 4
body2 = json.dumps(dict(hello="world4"))
print(body2)
cmd = 104
header = [ver, body2.__len__(), cmd]
headPack2 = struct.pack("!3I", *header)

sendData3 = headPack1 + body1.encode() + headPack2 + body2.encode()

# 正常数据包
client.send(sendData1)
time.sleep(3)

# 分包测试
client.send(sendData2_1)
time.sleep(0.2)
client.send(sendData2_2)
time.sleep(3)

# 粘包测试
client.send(sendData3)
time.sleep(3)
client.send(b"quit")
client.close()


while False:
	data = client.recv(1024)
	# 将bytes转为str输出
	print("[收到信息]", data.decode())
	msg = input("[发送信息]：")
	client.send(msg.encode())
	if msg == "quit":
		break
