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
import socket
import socketserver
import struct
import time
from threading import Thread

from Core import System
from Logic.HandleBasicMsg import HandleBasicMsg


class Connection(socketserver.BaseRequestHandler):
	clientAddress = []
	clientSockets = []

	def setup(self):
		self.dataBuffer = bytes()
		self.HEADER_SIZE = System.INT_SIZE
		self.packageNo = 0
		self.heartBeatTime = 30
		self.lastTickTime = time.time()
		self.request.settimeout(self.heartBeatTime)  # 对socket设置超时时间
		# 记录客户端地址
		print("[服务器] 客户端%s已连接" % str(self.client_address))
		# 保存到队列中
		self.clientAddress.append(self.client_address)
		self.clientSockets.append(self.request)

	def handle(self):
		sock = self.request
		sock.send("已连接服务器127.0.0.1:8888".encode())
		print("[服务器] 开始监听客户端消息")
		while True:
			try:
				data = sock.recv(1024)
			except socket.timeout:  # 超时会抛出socket.timeout异常
				print("[心跳检测] 超时，断开连接")
				sock.send("Quit")  # 这部分还没做完，还没主动发心跳包和退出消息
				break
			except ConnectionResetError:
				print("[服务器] 远程主机强迫关闭了一个现有的连接")
				break
			try:
				if data:  # 判断是否接收到数据
					self.processData(data)
			except ConnectionResetError:
				print("[服务器] 收到退出消息，客户端正常退出")
				break
		sock.close()

	def processData(self, data: bytes):
		"""用来处理消息，粘包分包，事件分发等功能。"""
		self.dataBuffer += data
		while True:
			# 若数据量不足够，则跳出循环接受下一次数据
			if len(self.dataBuffer) < self.HEADER_SIZE:
				print("[系统] 数据包（%s Byte）小于消息头部长度，等待下次接受" % len(self.dataBuffer))
				break
			# 读取header
			# headPack = struct.unpack('!I', self.dataBuffer[:self.HEADER_SIZE])
			bodySize = int.from_bytes(self.dataBuffer[:self.HEADER_SIZE], "big")
			# 分包情况处理，跳出函数继续接收数据
			if len(self.dataBuffer) < self.HEADER_SIZE + bodySize:
				print("[系统] 数据包（%s Byte）不完整（总共%s Byte），等待下次接受" % (len(self.dataBuffer), self.HEADER_SIZE + bodySize))
				break
			# 读取消息正文的内容
			print("[系统] 消息长度：%d" % bodySize)
			body = self.dataBuffer[self.HEADER_SIZE:self.HEADER_SIZE + bodySize]
			# 数据处理
			self.dataHandle(body)
			# 粘包情况处理（获取下一个数据包，类似于把数据pop出）
			self.dataBuffer = self.dataBuffer[self.HEADER_SIZE + bodySize:]

	def dataHandle(self, body):
		"""
		处理接受到的消息，如将json字符串反序列化，消息分发，反射调用事件
		:param body:
		:return:
		"""
		self.packageNo += 1
		print("第%s个数据包" % self.packageNo)
		name, start = System.GetString(body, 0)
		data = json.loads(body[start:])
		methodName = "Msg" + name
		# BasicMsg分发
		if name == "Register" or name == "Login" or name == "Quit":
			func = getattr(HandleBasicMsg, methodName, None)
			if not func:
				print("[警告] HandleMsg没有处理该方法：%s" % methodName)
				return
			print("[处理基础消息]", name)
			func(self.request, data)
		# PlayerMsg分发
		else:
			print("[处理玩家消息]", name)
			pass

	def finish(self):
		print("[服务器] 客户端连接已断开！")
		self.clientAddress.remove(self.client_address)
		self.clientSockets.remove(self.request)

	def Print(self):
		# 打印信息
		print("")
		print("===服务器登录信息===")
		print(self.clientAddress)


# 创建服务器（限制最大连接数）
HOST = "127.0.0.1"
PORT = 8888
IP_ADDRESS = HOST + ":" + str(PORT)
NWORKERS = 16
server = socketserver.ThreadingTCPServer((HOST, PORT), Connection)
print("[服务器]%s启动成功" % str(server.server_address))
# for n in range(NWORKERS):
# 	t = Thread(target=server.serve_forever)
# 	t.daemon = True
# 	t.start()
server.serve_forever()
