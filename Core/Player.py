# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
from Core import ServNet

class Player:
	def __init__(self, id, conn):
		self.id_ = id
		self.conn_ = conn
		self.data_ = None
		self.tempData_ = None

	def Send(self, protocol):
		if self.conn_ is None:
			return
		ServNet.Instance.Send(conn, protocol)

	def Kickoff(self, id, protocol):
		pass

	def Logout(self):
		pass