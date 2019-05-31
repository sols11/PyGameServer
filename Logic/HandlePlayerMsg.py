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

from Core import DataMgr, System


class HandlePlayerMsg:
	@classmethod
	def MsgUpdateInfo(cls, conn, bodyStr):
		data = System.JsonToData(bodyStr)
		if data is None:
			print("[系统] Data数据为空")
			return
		# data is a dict（python这边都会把json数据解析为dict）
		print(data["Id"])
		print(data["PosX"])

	@classmethod
	def MsgSave(cls, conn, bodyStr):
		DataMgr.Instance.SavePlayer("Anotts", bodyStr)
