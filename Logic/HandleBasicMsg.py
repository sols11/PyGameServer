# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/12
Description:

History:
----------------------------------------------------------------------------"""
import json
import socket

from Core import DataMgr


class HandleBasicMsg:
	@classmethod
	def MsgQuit(cls, conn: socket, data):
		"""
		客户端退出连接。协定用ConnectionResetError异常表示断开连接。
		消息函数都需要传递socket和json两个参数
		:param data:
		:param conn:
		:return:
		"""
		raise ConnectionResetError

	@classmethod
	def MsgRegister(cls, conn, data):
		"""
		处理注册信息的事件
		:param conn:
		:param data:
		:return:
		"""
		id = data["id"]
		pw = data["pw"]
		# 先不管是否能取到值
		print("[收到注册协议] 用户名：%s 密码：%s" % (id, pw))
		# 构建返回协议（0为成功）
		if DataMgr.Instance.Register(id, pw):
			conn.send(b"0")
			DataMgr.Instance.CreatePlayer(id)
		else:
			conn.send(b"-1")

	@classmethod
	def MsgLogin(cls, conn, jsonStr):
		data = json.loads(jsonStr)
		id = data["id"]
		pw = data["pw"]
		print("[收到登录协议] 用户名：%s 密码：%s" % (id, pw))
		if not DataMgr.Instance.CheckPassword(id, pw):
			conn.send("-1")
			return

	def MsgLogout(self):
		pass
