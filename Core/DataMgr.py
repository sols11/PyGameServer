# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
import re
import pymysql


class DataMgr:
	"""
	数据库封装.单例模式
	连接并不需要port
	"""

	def __init__(self):
		self.username_ = "root"
		self.password_ = "86696686"
		self.database_ = "game"
		self.db_ = None
		self.cursor_ = self.Connect()

	def Connect(self):
		self.db_ = pymysql.connect("localhost", self.username_, self.password_, self.database_)
		return self.db_.cursor()

	def IsSafeString(self, string):
		return not re.search(r"[-|;|,|\/|\(|\)|\[|\]|\}|\{|%|@|\*|!|\']", string)

	def CanRegister(self, id: str) -> bool:
		if not self.IsSafeString(id):
			return False
		query = r"SELECT * FROM USER WHERE ID='{}'".format(id)
		try:
			self.cursor_.execute(query)
			return self.cursor_.rowcount == 0
		except Exception:
			print("[DataMgr] CanRegister Fail:", Exception)

	def Register(self, id, pw) -> bool:
		if not self.IsSafeString(id) or not self.IsSafeString(pw):
			print("[DataMgr] Register 使用非法字符")
			return False
		if not self.CanRegister(id):
			print("[DataMgr] Register CanRegister")
			return False
		sql = r"INSERT INTO USER SET ID = '{0}' , PW = '{1}'".format(id, pw)
		try:
			self.cursor_.execute(sql)
			return True
		except Exception:
			print("[DataMgr] Register", Exception)
			return False

	def CreatePlayer(self, id) -> bool:
		if not self.IsSafeString(id):
			return False

	def CheckPassword(self, id, pw) -> bool:
		if not self.IsSafeString(id) or not self.IsSafeString(pw):
			return False
		query = r"SELECT * FROM USER WHERE ID='{0}' AND PW='{1};'".format(id, pw)
		try:
			self.cursor_.execute(query)
			return self.cursor_.rowcount != 0
		except Exception:
			print("[DataMgr] CheckPassword ", Exception)
			return False

	def GetPlayerData(self, id):
		if not self.IsSafeString(id):
			return None

	def SavePlayer(self, player):
		pass


Instance = DataMgr()
