# -*- coding: UTF-8 -*-

import socket
import random

sk = socket.socket()
ip_port = ("127.0.0.1", 8888)
sk.bind(ip_port)
sk.listen(5)  # max connections

while True:
    print("waiting for receiving data...")

    conn, address = sk.accept()
    msg = "建立连接"
    # python3网络传输的是bytes（字节），str需要进行编码 .encode()
    # python2同样，但str默认就是字节，所以不需要编码
    conn.send(msg.encode())
    while True:
        data = conn.recv(1024)  # 接收客户端信息
        print(data.decode())
        if data == b"quit":  # 接收到退出命令
            break
        conn.send("服务器收到".encode())
        conn.send(str(random.randint(1, 1024)).encode())  # 发送随机数据信息
    conn.close()



