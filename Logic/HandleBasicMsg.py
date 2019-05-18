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
from Core import DataMgr


class HandleBasicMsg:
	def MsgRegsiter(self, conn, jsonStr):
		"""
		处理注册信息的事件
		:param jsonStr:
		:return:
		"""
		data = json.loads(jsonStr)
		id = data["id"]
		pw = data["pw"]
		print("[收到注册协议] 用户名：%s 密码：%s" % (id, pw))
		# 构建返回协议
		if DataMgr.Instance.Register(id, pw):
			conn.send("0")
			DataMgr.Instance.CreatePlayer(id)
		else:
			conn.send("-1")

	def MsgLogin(self, conn, jsonStr):
		data = json.loads(jsonStr)
		id = data["id"]
		pw = data["pw"]
		print("[收到登录协议] 用户名：%s 密码：%s" % (id, pw))
		if not DataMgr.Instance.CheckPassword(id, pw):
			conn.send("-1")
			return

	def MsgLogout(self):
		pass


