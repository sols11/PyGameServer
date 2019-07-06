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
from Core import DataMgr, System, Navigation


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

	@classmethod
	def MsgNavigate(cls, conn, bodyStr):
		posList = System.JsonToData(bodyStr)
		if posList is None:
			print("[系统] Data数据为空")
			return
		pathList = Navigation.Navigate(posList[0], posList[1])
		# print(pathList)
		jsonStr = json.dumps(pathList)
		conn.send(System.CreatePackage("Navigate", System.ToBytes(jsonStr)))
