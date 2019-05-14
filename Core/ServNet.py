# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/12
Description:

History:
----------------------------------------------------------------------------"""
import socket
import sys
import threading

from Core.Conn import Conn


class ServNet:
	def __init__(self):
		self.listenfd_ = None
		self.conns_ = list()
		self.maxConn_ = 50
		self.timer_ = None
		self.heartBeatTime_ = 180
		self.proto_ = None
		self.handleConnMsg_ = None
		self.handlePlayerMsg_ = None
		self.handlePlayerEvent_ = None

	def GetConnIndex(self) -> int:
		"""
		从连接池获取可用连接，如果没有可用的连接会创建，超过上限则失败
		:return: 返回可用连接的索引，返回-1表示获取失败
		"""
		# 先查找可用的连接
		for i, conn in enumerate(self.conns_):
			if not conn.isUse_:
				return i
		if len(self.conns_) >= self.maxConn_:
			return -1
		self.conns_.append(Conn())
		return len(self.conns_) - 1

	def Start(self, host, port):
		# 定时器
		# Socket
		self.listenfd_ = socket.socket()
		self.listenfd_.bind((host, port))
		self.listenfd_.listen(self.maxConn_)
		print("[服务器]启动成功")
		try:
			while True:
				sock, addr = self.listenfd_.accept()
				print("[服务器]已连接，开始监听……")
				sock.send(b"Connected!")
				while True:
					data = sock.recv(1024)
					if data == b"quit":  # 接收到退出命令
						break
					sock.send(data)
					# 传输的是bytes，因此输出时我们将其转为str
					print("Server转发信息：" + data.decode())
				sock.close()
		finally:
			self.listenfd_.close()

	def AcceptCb(self):
		try:
			sock, addr = self.listenfd_.accept()
			index = self.GetConnIndex()
			if index < 0:
				sock.close()
				print("[警告]链接已满")
			else:
				conn = self.conns_[index]
				conn.Init(sock)
				print("客户端连接[", addr, "] conn池ID：", index)
				sock.beginRecv(1024)
			self.listenfd_.beginAccept()
		except RuntimeError as e:
			print("Accept失败：" + e.args)

	def Close(self):
		for conn in self.conns_:
			if conn and conn.isUse_:
				conn.Close()

	def processData(self, conn):
		if conn.buffCount_ < sys.getsizeof(int):
			return


Instance = ServNet()
