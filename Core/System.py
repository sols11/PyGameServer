# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:
	协定int为4个字节，即使用Int32。使用大端传输
	提供辅助方法。如消息打包，字节流操作，类型转换……
History:
----------------------------------------------------------------------------"""
import struct
import json

INT_SIZE = 4


def CreatePackage(name: str, body: str or bytes = b""):
	"""
	Send之前都需要先打包，无论body是使用字节流还是Json传输，都可以用这个API打包后发送
	我们设置包协议为 int(消息长度) + name(int+str消息名称) + str
	:param name:
	:param body:
	:return:
	"""
	body = len(name).to_bytes(INT_SIZE, "big") + name.encode() + ToBytes(body)
	size = len(body)
	headPack = size.to_bytes(INT_SIZE, "big")  # 用to_bytes代替struct打包
	# header = [size]
	# headPack = struct.pack("!I", *header)
	package = headPack + body
	return package


def JsonToData(jsonStr):
	"""
	解析Json字符串并返回data，失败抛出JSONDecodeError异常
	:param jsonStr:
	:return:
	"""
	try:
		if jsonStr:
			data = json.loads(jsonStr)
		else:
			data = None
	except json.decoder.JSONDecodeError:
		print("[系统] JSON数据解析错误")
		data = None
	return data


def AddInt(body: bytes, num: int):
	return body + num.to_bytes(INT_SIZE, "big")


def GetInt(body: bytes, start: int) -> tuple:
	"""
	返回指定位置拿到的int数据和end下标，若没拿到抛出异常
	:param body:
	:param start:
	:return: tuple
	"""
	end = start + INT_SIZE
	if len(body) < end:
		raise ValueError("获取int数据失败")
	num = int.from_bytes(body[start:end], "big")
	return num, end


def AddString(body: bytes, string: str):
	size = len(string)
	body += size.to_bytes(INT_SIZE, "big") + string.encode()
	return body


def GetString(body: bytes, start: int) -> tuple:
	"""
	返回指定位置拿到的string数据和end下标，若没拿到抛出异常
	:param body:
	:param start:
	:return: tuple
	"""
	try:
		size, start = GetInt(body, start)
	except ValueError:
		raise BufferError("获取string的size数据失败")
	else:
		end = start + size  # 还需要计算出string的end索引
		if len(body) < end:
			raise BufferError("获取string内容数据失败")
		return body[start:end].decode(), end


def ToStr(bytesOrStr):
	"""
	将参数转为str返回
	:param bytesOrStr:
	:return:
	"""
	if isinstance(bytesOrStr, bytes):
		value = bytesOrStr.decode('utf-8')
	else:
		value = bytesOrStr
	return value  # instance of str


def ToBytes(bytesOrStr):
	"""
	将参数转为bytes返回
	:param bytesOrStr:
	:return:
	"""
	if isinstance(bytesOrStr, str):
		value = bytesOrStr.encode('utf-8')
	else:
		value = bytesOrStr
	return value  # instance of bytes
