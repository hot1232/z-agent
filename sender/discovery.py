#!/usr/bin/env python
# -*- coding:utf8 -*-

import struct

class Sender(object):
    def __init__(self,socket=None,data=None):
        self.data=data
        self.data_len=struct.pack('<Q', len(data))
        self.header="ZBXD\1"
        self.socket=socket
    
    def send(self):
        self.socket.sendall(self.header+self.data_len+self.data)