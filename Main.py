# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/30
Description:
   启动文件
History:
----------------------------------------------------------------------------"""
import socketserver
from Core.Connection import Connection


# 创建服务器（限制最大连接数）

HOST = "127.0.0.1"
PORT = 8888
IP_ADDRESS = HOST + ":" + str(PORT)
NWORKERS = 16
server = socketserver.ThreadingTCPServer((HOST, PORT), Connection)
print("[服务器]%s启动成功" % str(server.server_address))
# for n in range(NWORKERS):
# 	t = Thread(target=server.serve_forever)
# 	t.daemon = True
# 	t.start()
server.serve_forever()
input()
