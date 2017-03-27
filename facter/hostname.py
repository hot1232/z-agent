#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
from . import FacterBase
import socket

class Facter(FacterBase):
    def _init(self):
        pass
    
    def facter_hostname(self):
        return os.uname()[1]
    
    def facter_os_type(self):
        return os.uname()[0]    
    
    def facter_fqdn(self):
        return socket.getfqdn()

if __name__ == "__main__":
    print os.uname()[1]