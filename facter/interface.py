#!/usr/bin/env python
# -*- coding:utf8 -*-

from . import FacterBase

class Facter(FacterBase):
    def facter_interfaces(self):
        with open("/proc/net/dev", "r") as f:
            _ = f.readlines(2)
            line = f.readline()
            interfaces = []
            while line:
                interfaces.append(line.split()[0])
                line = f.readline()
        return interfaces
    