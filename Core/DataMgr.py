# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:
	数据库封装.单例模式
	连接mysql并不需要port
History:
----------------------------------------------------------------------------"""
import re
import pymysql


class DataMgr:

	def __init__(self):
		self.username_ = "root"
		self.password_ = "123321"
		self.database_ = "pygameserver"
		self.db_ = None
		self.cursor_ = None
		self.connect()

	def __delete__(self, instance):
		if self.db_ is not None:
			self.db_.commit()
			self.db_.close()

	def connect(self):
		self.db_ = pymysql.connect("localhost", self.username_, self.password_)
		self.cursor_ = self.db_.cursor()
		self.CreateSchema()

	def IsSafeString(self, string):
		return not re.search(r"[-|;|,|\/|\(|\)|\[|\]|\}|\{|%|@|\*|!|\']", string)

	def CreateSchema(self):
		sql = r"CREATE SCHEMA `pygameserver`;"
		try:
			self.cursor_.execute(sql)
		except:
			print("[DataMgr] 数据库已存在")
			self.db_.rollback()
			self.cursor_.execute(r"use pygameserver")
			return
		else:
			self.cursor_.execute(r"use pygameserver")
		sql = r"""CREATE TABLE `pygameserver`.`user` (
  `id` VARCHAR(10) NOT NULL DEFAULT '1',
  `pw` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`));"""
		try:
			self.cursor_.execute(sql)
		except:
			print("[DataMgr] 表格已创建")
			self.db_.rollback()
		self.db_.commit()

	def CanRegister(self, id: str) -> bool:
		if not self.IsSafeString(id):
			print("[DataMgr] CanRegister 使用非法字符")
			return False
		query = r"SELECT * FROM USER WHERE ID='{}'".format(id)
		try:
			self.cursor_.execute(query)
			return self.cursor_.rowcount == 0
		except:
			print("[DataMgr] 注册查询失败:")
			return False

	def Register(self, id, pw) -> bool:
		if not self.IsSafeString(id) or not self.IsSafeString(pw):
			print("[DataMgr] Register 使用非法字符")
			return False
		if not self.CanRegister(id):
			print("[DataMgr] Register 不可注册")
			return False
		sql = r"INSERT INTO USER SET ID = '{0}' , PW = '{1}'".format(id, pw)
		try:
			self.cursor_.execute(sql)
		except:
			print("[DataMgr] 注册失败:")
			self.db_.rollback()
			return False
		self.db_.commit()
		# self.CreatePlayer(id)
		return True

	def CheckPassword(self, id, pw) -> bool:
		if not self.IsSafeString(id) or not self.IsSafeString(pw):
			print("[DataMgr] CheckPassword 使用非法字符")
			return False
		query = r"SELECT * FROM USER WHERE ID='{0}' AND PW='{1}';".format(id, pw)
		try:
			self.cursor_.execute(query)
			return self.cursor_.rowcount != 0
		except:
			print("[DataMgr] 密码查询失败")
			return False

	# Player相关操作
	def CreatePlayer(self, id):
		sql = r"INSERT INTO `pygameserver`.`player` (`id`) VALUES ('{0}');".format(id)
		try:
			self.cursor_.execute(sql)
			return True
		except:
			print("[DataMgr] 创建角色失败:")
			self.db_.rollback()
			return False

	def LoadPlayer(self, id):
		if not self.IsSafeString(id):
			return None
		query = r"SELECT * FROM PLAYER WHERE ID='{}'".format(id)
		try:
			self.cursor_.execute(query)
			return self.cursor_.rowcount == 0
		except:
			print("[DataMgr] 读档失败:")
			return False

	def SavePlayer(self, id, xmlStr):
		sql = r"UPDATE `pygameserver`.`player` SET `data` = '{0}'  WHERE (`id` = '{1}')".format(xmlStr, id)
		try:
			self.cursor_.execute(sql)
			return True
		except:
			print("[DataMgr] 保存失败")
			self.db_.rollback()
			raise
			return False


Instance = DataMgr()
