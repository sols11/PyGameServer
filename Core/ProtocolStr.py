# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""
from Core import ProtocolBase


class ProtocolStr(ProtocolBase):
    """	 
    字符串协议模型
    形式：名称,参数1,参数2,参数3
    一般只有纯字符串发送时才会用
    """

    def __init__(self):
        self.str_ = str()

    def Decode(self, readbuff: bytes, start, length) -> ProtocolBase:
        protocol = ProtocolStr()
        protocol.str_ = readbuff[start:start + length].decode()
        return protocol

    def Encode(self):
        return self.str_.encode()

    # 协议名称
    def GetName(self):
        if len(self.str_) == 0:
            return ""
        return self.str_.split(',')[0]

    # 协议描述
    def GetDesc(self):
        return self.str_
