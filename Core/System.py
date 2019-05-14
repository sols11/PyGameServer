# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
import time

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
