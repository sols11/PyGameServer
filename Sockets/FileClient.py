# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/05/29
Description:

History:
----------------------------------------------------------------------------"""
import socket, os
import json


class FTP_Client(object):
	def __init__(self):
		self.ftp_socket = socket.socket()

	def connection(self, ADDR):
		self.ftp_socket.connect(ADDR)

	def help(self):
		msg = {
			'get filename',
			'put filename'
		}
		print('the use of ftp is:', msg)

	# 客户端的接口，利用反射进行具体的上传和下载功能
	def interactive(self):
		while True:
			cmd = input('>>:').strip()  # strip()函数功能可以实现对字符串头部和尾部的空格和换行符进行删除处理
			if len(cmd) == 0:
				continue
			cmd_order = cmd.split()[0]
			# 利用反射选择到底是执行上传功能还是下载功能
			if hasattr(self, 'cmd_%s' % cmd_order):
				func = getattr(self, 'cmd_%s' % cmd_order)
				func(cmd)
			else:
				self.help()

	# 上传文件
	def cmd_put(self, *argv):
		cmd_str = argv[0].split()  # 客户端输入的命令
		if len(cmd_str) > 1:
			filename = cmd_str[1]  # 上传文件的文件名
			if os.path.isfile(filename):  # 如果当前路径下存在该文件
				# 以json的格式将上传文件的相关信息发送过去
				file_size = os.stat(filename).st_size
				msg_dic = {
					'action': 'put',
					'filename': filename,
					'size': file_size,
					'overloaded': False
				}
				self.ftp_socket.send(json.dumps(msg_dic).encode())
				# 防止粘包，等待客户端确认
				server_response = self.ftp_socket.recv(1024).decode()
				print(server_response)
				# 发送文件
				f = open(filename, 'rb')
				for line in f:
					self.ftp_socket.send(line)
				else:
					print('%s has been sent over' % filename)
				f.close()
			else:
				print('the %s is not exisit' % filename)
		else:
			self.help()

	# 下载文件
	def cmd_get(self, *argv):
		cmd_str = argv[0].split()
		if len(cmd_str) > 1:
			action = cmd_str[0]
			filename = cmd_str[1]
			msg_dic = {
				'action': action,
				'filename': filename,
				'overloaded': False
			}
			self.ftp_socket.send(json.dumps(msg_dic).encode())
			# 接收文件的大小
			file_size = int(self.ftp_socket.recv(1024).decode())
			# 向服务器端发送准备接收文件的命令
			self.ftp_socket.send(b'400 OK!')
			received_size = 0
			# 检测客户端是否存在该文件
			if os.path.isfile(filename):
				f = open(filename + '.new', 'wb')
			else:
				f = open(filename, 'wb')
			while received_size < file_size:
				file_data = self.ftp_socket.recv(1024)
				f.write(file_data)
				received_size += len(file_data)
			else:
				print('%s has been loaded' % filename)
		else:
			self.help()


Ftp_Client = FTP_Client()
Ftp_Client.connection(("0.0.0.0", 8889))
Ftp_Client.interactive()
