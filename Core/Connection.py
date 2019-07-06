# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/12
Description:
   SocketServer是每连接一个客户端就会创建一个SocketServer实例，因此这更像是一个Connection。
History:
----------------------------------------------------------------------------"""
import socket
import socketserver
import time

from Core import System
from Logic.HandlePlayerMsg import HandlePlayerMsg
from Logic.HandleBasicMsg import HandleBasicMsg


class Connection(socketserver.BaseRequestHandler):
	ClientAddress = []
	ClientSockets = []

	def setup(self):
		"""
		socketserver初始化设置
		:return:
		"""
		self.dataBuffer_ = bytes()
		self.HEADER_SIZE = System.INT_SIZE
		self.heartBeatTime_ = 120
		self.navTimer_ = time.perf_counter()
		self.request.settimeout(self.heartBeatTime_)  # 对socket设置超时时间
		# 记录客户端地址
		print("[服务器] 客户端%s已连接" % str(self.client_address))
		# 保存到队列中
		self.ClientAddress.append(self.client_address)
		self.ClientSockets.append(self.request)

	def handle(self):
		"""
		建立连接，接受消息，处理消息，心跳检测，关闭连接
		:return:
		"""
		sock = self.request
		print("[服务器] 开始监听客户端消息")
		while True:
			try:
				data = sock.recv(1024)
			except socket.timeout:  # 超时会抛出socket.timeout异常
				print("[心跳检测] 超时，断开连接")
				sock.send(System.CreatePackage("Disconnect"))
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
		self.dataBuffer_ += data
		while True:
			# 若数据量不足够，则跳出循环接受下一次数据
			if len(self.dataBuffer_) < self.HEADER_SIZE:
				print("[系统] 数据包（%s Byte）小于消息头部长度，等待下次接受" % len(self.dataBuffer_))
				break
			# 读取header
			bodySize = int.from_bytes(self.dataBuffer_[:self.HEADER_SIZE], "big")
			# 分包情况处理，跳出函数继续接收数据
			if len(self.dataBuffer_) < self.HEADER_SIZE + bodySize:
				print("[系统] 数据包（%s Byte）不完整（总共%s Byte），等待下次接受" % (len(self.dataBuffer_), self.HEADER_SIZE + bodySize))
				break
			# 读取消息正文的内容
			print("[系统] 消息长度：%d" % bodySize)
			body = self.dataBuffer_[self.HEADER_SIZE:self.HEADER_SIZE + bodySize]
			# 数据处理
			self.dataHandle(body)
			# 粘包情况处理（获取下一个数据包，类似于把数据pop出）
			self.dataBuffer_ = self.dataBuffer_[self.HEADER_SIZE + bodySize:]

	def dataHandle(self, body):
		"""
		处理接受到的消息，如将json字符串反序列化，消息分发，反射调用事件
		:param body:
		:return:
		"""
		name, start = System.GetString(body, 0)
		bodyStr = body[start:]
		methodName = "Msg" + name
		# BasicMsg分发
		if name == "Register" or name == "Login" or name == "Disconnect" or name == "HeartBeat":
			func = getattr(HandleBasicMsg, methodName, None)
			if not func:
				print("[警告] HandleMsg没有处理该方法：%s" % methodName)
				return
			print("[处理基础消息]", name)
			func(self.request, bodyStr)
		# PlayerMsg分发
		else:
			func = getattr(HandlePlayerMsg, methodName, None)
			if not func:
				print("[警告] HandleMsg没有处理该方法：%s" % methodName)
				return
			print("[处理玩家消息]", name)
			func(self.request, bodyStr)

	def finish(self):
		print("[服务器] 客户端连接已断开！")
		self.ClientAddress.remove(self.client_address)
		self.ClientSockets.remove(self.request)

	def Print(self):
		# 打印信息
		print("")
		print("===服务器登录信息===")
		print(self.ClientAddress)


# 创建服务器（限制最大连接数）
if __name__ == "__main__":
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
