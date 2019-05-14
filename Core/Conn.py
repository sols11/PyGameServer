# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
import time


class Conn:
	"""
	连接类，用于维持客户端连接
	"""

	def __init__(self):
		self.BUFFER_SIZE_ = 1024
		self.socket_ = None
		# 是否使用
		self.isUse_ = False
		# Buffer
		self.readBuff_ = bytes()
		self.buffCount_ = 0
		# 粘包分包
		self.msgLength_ = 0
		# 心跳时间
		self.lastTickTime_ = -1
		# 对应的Player
		self.player_ = None

	def Init(self, socket):
		self.socket_ = socket
		self.isUse_ = True
		self.buffCount_ = 0
		# 心跳处理
		self.lastTickTime_ = time.time()

	def BuffRemain(self):
		return self.BUFFER_SIZE_ - self.buffCount_

	def GetAddress(self):
		if not self.isUse_:
			return "无法获取地址"
		return  # socket.RemoteEndPoint.ToString();

	def Close(self):
		# 正在使用
		if not self.isUse_:
			return
		if self.player_ is not None:
			self.player_.Logout()
			return
		print("[断开连接]", self.GetAddress())
		# self.socket_.Close()
		self.isUse_ = False

	def Send(self, protocol):
		# ServNet.Instance.Send(protocol)
		pass