# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
import struct


# 我们设置包头为一个int数据，记录消息长度
def CreateHeadPack(size: int = 0):
	header = [size]
	headPack = struct.pack("!I", *header)
	return headPack


def ToStr(bytesOrStr):
	if isinstance(bytesOrStr, bytes):
		value = bytesOrStr.decode('utf-8')
	else:
		value = bytesOrStr
	return value  # instance of str


def ToBytes(bytesOrStr):
	if isinstance(bytesOrStr, str):
		value = bytesOrStr.encode('utf-8')
	else:
		value = bytesOrStr
	return value  # instance of bytes


class System:
	def GetTimeStamp(self):
		pass
