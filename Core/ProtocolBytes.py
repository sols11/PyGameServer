# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
from Core import ProtocolBase
import sys


class ProtocolBytes(ProtocolBase):
	"""
	字节流协议模型
	"""
	def __init__(self):
		self.bytes_ = bytes()

	def Decode(self, readbuff: bytes, start, length) -> ProtocolBase:
		protocol = ProtocolBytes()
		protocol.bytes_ = readbuff[start:start + length]
		return protocol

	def Encode(self):
		return self.bytes_

	def GetName(self):
		return self.GetString(0)

	def GetDesc(self):
		desc = str()
		if len(self.bytes_) == 0:
			return desc
		for b in self.bytes_:
			desc += str(int(b)) + " "
		return desc

	def AddString(self, string: str):
		"""
		添加字符串。先添加字符串长度信息，再加入字符串。
		:param string:
		:return:
		"""
		strLength = len(string)
		# if len(self.bytes_) == 0:
		self.bytes_ += bytes(strLength) + string.encode()

	def GetString(self, start):
		"""
		从字节数组的start处开始读取字符串
		:param start:
		:return:
		"""
		end = start + sys.getsizeof(int) + self.GetInt(start)[0]  # 长度为int+int记录的长度
		if len(self.bytes_) < end:
			return bytes(), 0
		return str(self.bytes_[start:end]), end

	def AddInt(self, num):
		self.bytes_ += bytes(num)

	def GetInt(self, start) -> tuple:
		"""
		安全方式获取，失败返回0
		:param start:
		:return:
		"""
		end = start + sys.getsizeof(int)
		if len(self.bytes_) < end:
			return 0, 0
		return int(self.bytes_[start:end]), end

	def AddFloat(self, num):
		self.bytes_ += bytes(num)

	def GetFloat(self, start) -> tuple:
		"""
		安全方式获取，失败返回0
		:param start:
		:return:
		"""
		end = start + sys.getsizeof(float)
		if len(self.bytes_) < end:
			return 0, 0
		return int(self.bytes_[start:end]), end
