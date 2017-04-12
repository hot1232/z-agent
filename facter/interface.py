#!/usr/bin/env python
# -*- coding:utf8 -*-

from . import FacterBase

class Facter(FacterBase):
    def _init(self):
        self.interfaces=[]
        self.facter_interfaces()
        
    def facter_interfaces(self):
        with open("/proc/net/dev", "r") as f:
            _ = f.readlines(2)
            line = f.readline()
            while line:
                self.interfaces.append(line.split()[0])
                line = f.readline()
        return self.interfaces
    
    
    