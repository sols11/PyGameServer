# -*- coding:UTF-8 -*-

import socket

class Client:

    def __init__(self, socket):
        self.clientSocket = socket
        # 咔，python怎么开线程啊，不管了先用C#弄出原型，熟练了再来
        pass

client = socket.socket()
ip_port = ("127.0.0.1", 8888)
client.connect(ip_port)

while True:
    data = client.recv(1024)
    print(data.decode())  # python3需要.decode()
    msg_input = input("请输入发送的信息：")
    # 发送消息
    client.send(msg_input.encode())
    if msg_input == "quit":
        break
    data = client.recv(1024)
    print(data.decode())
