#!/usr/bin/env python
# -*- coding:utf8 -*-

import struct
from lib.log import logging
import json

class Sender(object):
    def __init__(self,socket=None,data=None):
        self.data=json.dumps(data)
        self.data_len=struct.pack('<Q', len(self.data))
        self.header="ZBXD\1"
        self.socket=socket
        self.logger=logging.getLogger(__name__)
    
    def send(self):
        self.socket.sendall(self.header+self.data_len+self.data)