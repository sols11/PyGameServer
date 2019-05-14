# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
from Core import DataMgr
from Core import ServNet

if __name__ == "__main__":
	dataMgr = DataMgr.Instance
	servNet = ServNet.Instance
	# servNet.proto_ = ProtocolBytes.ProtocolBytes()
	servNet.Start("127.0.0.1", 8888)
	# servNet.serve_forever()  # 激活服务器，会一直运行，直到Ctrl-C中断
	while False:
		servInput = input()
		if servInput == "quit":
			servNet.Close()
			break
		elif servInput == "print":
			servNet.Print()
