# -*- coding: UTF-8 -*-

import socket
import random

sk = socket.socket()
ip_port = ("127.0.0.1", 8888)
sk.bind(ip_port)
sk.listen(5)  # max connections

while True:
    print("waiting for receiving data...")
    msg = "建立连接"
    # python3网络传输的是bytes（字节），str需要进行编码 .encode()
    # python2同样，但str默认就是字节，所以不需要编码
    while True:
        conn, address = sk.accept()
        print("新客户端连接")

