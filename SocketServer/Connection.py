# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/12
Description:
   鉴于之前C#服务端的实现比较难和SocketServer兼容，因此自己实现一套连接方式。
   SocketServer是每连接一个客户端就会创建一个SocketServer实例，因此这更像是一个Connection。
History:
----------------------------------------------------------------------------"""
import json
import socketserver
import struct
import time
from threading import Thread


class Connection(socketserver.BaseRequestHandler):
	def setup(self):
		print(self.server)
		ip = self.client_address[0].strip()  # 获取客户端的ip
		port = self.client_address[1]  # 获取客户端的port
		print("[服务器] 客户端", ip + ":" + str(port), "已连接")
		self.dataBuffer = bytes()
		self.headerSize = 12
		self.sn = 0
		self.heartBeatTime = 30
		self.lastTickTime = time.time()

	def handle(self):
		sock = self.request
		sock.send("已连接服务器127.0.0.1:8888".encode())
		print("[服务器] 开始监听客户端消息")
		while True:
			data = sock.recv(1024)
			print("[收到信息]", data.decode())
			self.processData(data)
			if data == b"quit":
				break
			sock.send("信息已接收".encode())
		sock.close()

	def createHeadPack(self):
		ver = 1
		body = json.dumps(dict(hello = "world"))
		print(body)  # {"hello": "world"}
		cmd = 101
		header = [ver, len(body), cmd]
		headPack = struct.pack("!3I", *header)
		print(headPack)  # b'\x00\x00\x00\x01\x00\x00\x00\x12\x00\x00\x00e'

	def processData(self, data: bytes):
		"""用来处理消息，粘包分包，事件分发等功能。"""
		self.dataBuffer += data
		while True:
			if len(self.dataBuffer) < self.headerSize:
				print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(self.dataBuffer))
				break
			# 读取header
			headPack = struct.unpack('!3l', self.dataBuffer[:self.headerSize])
			bodySize = headPack[1]
			# 分包情况处理，跳出函数继续接收数据
			if len(self.dataBuffer) < self.headerSize + bodySize:
				print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), self.headerSize + bodySize))
				break
			# 读取消息正文的内容
			body = self.dataBuffer[self.headerSize:self.headerSize + bodySize]
			# 数据处理
			self.dataHandle(headPack, body)
			# 粘包情况处理
			dataBuffer = self.dataBuffer[self.headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出

	def dataHandle(self, headPack, body):
		self.sn += 1
		print("第%s个数据包" % self.sn)
		print("ver:%s, bodySize:%s, cmd:%s" % headPack)
		print(body.decode())
		print()

	def finish(self):
		pass


# 创建服务器（限制最大连接数）
HOST = "127.0.0.1"
PORT = 8888
IP_ADDRESS = HOST + ":" + str(PORT)
NWORKERS = 16
server = socketserver.ThreadingTCPServer((HOST, PORT), Connection)
print("[服务器]", server.server_address, "启动成功")
for n in range(NWORKERS):
	t = Thread(target=server.serve_forever)
	t.daemon = True
	t.start()
server.serve_forever()
