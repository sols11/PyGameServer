# -*- coding: UTF-8 -*-
"""----------------------------------------------------------------------------
Author:
   caodahan97@126.com
Date:
   2019/04/24
Description:

History:
----------------------------------------------------------------------------"""


class ProtocolBase:
    """协议基类"""

    # 解码器，解码readbuff中从start开始的length字节
    def Decode(self, readbuff, start, length):
        return ProtocolBase()

    # 编码器
    def Encode(self):
        return b""

    # 协议名称，用于消息分发
    def GetName(self):
        return ""

    # 描述
    def GetDesc(self):
        return ""
