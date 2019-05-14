# -*- coding: UTF-8 -*-

import socketserver
import random
import threading

client_addr = []


class ChatServer(socketserver.BaseRequestHandler):

	def setup(self):
		ip = self.client_address[0].strip()  # 获取客户端的ip
		port = self.client_address[1]  # 获取客户端的port
		print(ip + ":" + str(port) + " is connect!")
		client_addr.append(self.client_address)  # 保存到队列中

	def handle(self):
		conn = self.request
		msg = "建立连接"
		conn.send(msg.encode())
		print("新客户端连接")
		while True:
			self.data = conn.recv(1024).decode().strip()
			print(self.data)
			curThread = threading.current_thread()
			if self.data == "quit":
				break
			conn.send("服务器收到".encode())
			conn.sendall(bytes("{}: {}".format(curThread.name, self.data), 'ascii'))
		conn.close()

	def BroadcastMsg(self, msg):
		pass

	def finish(self):
		pass


if __name__ == "__main__":
	server = socketserver.ThreadingTCPServer(("127.0.0.1", 8888), ChatServer)
	print("服务器开始监听……")
	server.serve_forever()  # 激活服务器，会一直运行，直到Ctrl-C中断
