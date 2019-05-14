# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/12
Description:
   鉴于之前C#服务端的实现比较难和SocketServer兼容，因此自己实现一套连接方式。
   SocketServer是每连接一个客户端就会创建一个SocketServer实例，因此这更像是一个Connection。
History:
----------------------------------------------------------------------------"""
import socketserver
import threading


class Connection(socketserver.BaseRequestHandler):
	def setup(self):
		print(self.server)
		ip = self.client_address[0].strip()  # 获取客户端的ip
		port = self.client_address[1]  # 获取客户端的port
		print("[服务器] 客户端", ip + ":" + str(port), "已连接")

	def handle(self):
		sock = self.request
		sock.send("已连接服务器127.0.0.1:8888".encode())
		print("[服务器] 开始监听客户端消息")
		while True:
			data = sock.recv(1024)
			print("[收到信息]", data.decode())
			if data == b"quit":
				break
			sock.send("信息已接收".encode())
		sock.close()

	def finish(self):
		pass


# 创建服务器
server = socketserver.ThreadingTCPServer(("127.0.0.1", 8888), Connection)
print("[服务器]", "127.0.0.1:8888", "启动成功")
server.serve_forever()
