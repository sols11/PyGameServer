# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/29
Description:
	Server：得到client的json包，执行对应方法，如put即发送确认接受应答，然后循环写入文件。
	get则将文件发送出去
History:
----------------------------------------------------------------------------"""
import socketserver
import os
import json


class FileServer(socketserver.BaseRequestHandler):
	def handle(self):
		while True:
			try:
				# 接受客户端发送过来的指令
				self.data = self.request.recv(1024).strip()
				# 打印客户端的链接地址
				print('the client address is', '{}:'.format(self.client_address[0]))
				# 利用json包解析发送过来的命令
				cmd_dir = json.loads(self.data.decode())
				cmd = cmd_dir['action']

				# 利用反射的原理，根据客户端发送过来的指令，决定是执行上传还是下载命令
				if hasattr(self, cmd):
					func = getattr(self, cmd)
					func(cmd_dir)
			except ConnectionResetError as e:
				print('err', e)
				break

	def put(self, *argv):
		"""
		接受客户端发送的文件，从参数中得到文件名、大小
		:param argv:
		:return:
		"""
		argv_ = argv[0]
		cmd_str = argv_
		filename = cmd_str['filename']
		file_size = cmd_str['size']
		# 检测服务器端是否存在该文件；如果存在重新命名
		if os.path.isfile(filename):
			f = open(filename + '.new', 'wb')
		else:
			f = open(filename, 'wb')

		# 向客户端发送已经准备好可以接受数据了
		self.request.send(b'UPLOAD!')
		received_size = 0  # 已经接受的数据大小
		# 循环接受，写入文件，直到结束
		while received_size < file_size:
			file_data = self.request.recv(1024)
			f.write(file_data)
			received_size += len(file_data)
		else:
			print('%s has been loaded over' % filename)

	def get(self, *argv):
		"""
		客户端从服务端下载指定的文件
		:param argv:
		:return:
		"""
		cmd_str = argv[0]
		filename = cmd_str['filename']
		# 检测服务器端是否存在需要下载的文件
		if os.path.isfile(filename):
			file_size = os.stat(filename).st_size
			# 发送size再等待反馈
			self.request.send(str(file_size).encode())
			client_response = self.request.recv(1024).decode()
			print('client response is %s' % client_response)
			f = open(filename, 'rb')
			# 逐行发送
			for line in f:
				self.request.send(line)
			else:
				print('%s has been sent over' % filename)
			f.close()
		else:
			print('%s is not exisiting in server' % filename)


FtpServer = socketserver.TCPServer(("127.0.0.1", 8889), FileServer)
print('waiting for connection...')
FtpServer.serve_forever()
