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

from Core import DataMgr, System


class HandleBasicMsg:
	@classmethod
	def MsgHeartBeat(cls, conn, bodyStr):
		# 让client每隔一定时间发一个name为HeartBeat的消息，即为心跳
		print("[更新心跳时间]")

	@classmethod
	def MsgOther(cls, conn, bodyStr):
		pass

	@classmethod
	def MsgDisconnect(cls, conn: socket, bodyStr: dict):
		"""
		客户端退出连接。协定用ConnectionResetError异常表示断开连接。
		消息函数都需要传递socket和json两个参数
		:param data:
		:param conn:
		:return:
		"""
		raise ConnectionResetError

	@classmethod
	def MsgRegister(cls, conn, bodyStr):
		"""
		处理注册信息的事件
		:param conn:
		:param data:
		:return:
		"""
		data = System.JsonToData(bodyStr)
		if data is None:
			print("[系统] Data数据为空")
			conn.send(System.CreatePackage("Register", b"-1"))
			return
		id = data["id"]
		pw = data["pw"]
		# 先不管是否能取到值
		print("[收到注册协议] 用户名：%s 密码：%s" % (id, pw))
		# 构建返回协议（0为成功）
		if DataMgr.Instance.Register(id, pw):
			conn.send(System.CreatePackage("Register", b"0"))
			DataMgr.Instance.CreatePlayer(id)
		else:
			conn.send(System.CreatePackage("Register", b"-1"))

	@classmethod
	def MsgLogin(cls, conn, bodyStr):
		data = System.JsonToData(bodyStr)
		if data is None:
			print("[系统] Data数据为空")
			conn.send(System.CreatePackage("Register", b"-1"))
			return
		id = data["id"]
		pw = data["pw"]
		print("[收到登录协议] 用户名：%s 密码：%s" % (id, pw))
		if not DataMgr.Instance.CheckPassword(id, pw):
			conn.send(System.CreatePackage("Login", b"-1"))
			return
		pass
		conn.send(System.CreatePackage("Login", b"0"))

	@classmethod
	def MsgLogout(cls, conn, bodyStr):
		sendData = System.CreatePackage("Logout")
		conn.send(sendData)
