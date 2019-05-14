# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
import socketserver
import threading

from Core.Conn import Conn


class ServNet(socketserver.BaseRequestHandler):
	def setup(self):
		self.ip_ = self.client_address[0].strip()  # 获取客户端的ip
		self.port_ = self.client_address[1]        # 获取客户端的port
		print(self.ip_ + ":" + str(self.port_) + " is connect!")
		self.conns_ = list()
		self.maxConn_ = 50
		self.timer_ = None
		self.heartBeatTime_ = 180
		self.proto_ = None

	def getConnection(self) -> Conn:
		"""
		从连接池获取可用连接，返回None表示获取失败
		:return:
		"""
		# 先查找可用的连接
		for conn in self.conns_:
			if not conn.isUse_:
				return conn
		if len(self.conns_) >= self.maxConn_:
			return None
		newConn = Conn()
		self.conns_.append(newConn)
		return newConn


	def handle(self):
		conn = self.getConnection()
		curThread = threading.current_thread()
		if not conn:
			print("[警告] 连接已满")
			return
		conn.Init(self.request)
		data = conn.socket_.recv(1024).decode().strip()
		response = bytes("{}: {}".format(curThread.name, data), 'ascii')
		self.request.sendall(response)


Instance = socketserver.ThreadingTCPServer(("127.0.0.1", 8888), ServNet)
