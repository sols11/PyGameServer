# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/12
Description:
	最简socket服务器
History:
----------------------------------------------------------------------------"""
import socket

server = socket.socket()
server.bind(("127.0.0.1", 8888))
server.listen(5)

try:
	while True:
		print("Waiting for connecting...")
		sock, addr = server.accept()
		sock.send(b"Connected!")
		while True:
			data = sock.recv(1024)
			if data == b"quit":  # 接收到退出命令
				break
			sock.send(data)
			# 传输的是bytes，因此输出时我们将其转为str
			print("Server转发信息：" + data.decode())
		sock.close()
finally:
	server.close()
