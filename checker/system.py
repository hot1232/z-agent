#!/usr/bin/env python
# -*- coding:utf8 -*-
#
__author__='liang.zhang'

from . import CheckerBase
import time
import os

class Checker(CheckerBase):
    def _init(self):
        self.interval=360
    def do_check_hostname(self):
        return os.uname()[1]
    def do_check_uptime(self):
        uptime=0
        with open("/proc/uptime","r") as f:
            uptime=float(f.readline().split()[0])
        return uptime
    def do_check_boottime(self):
        btime=""
        with open("/proc/stat","r") as f:
            for line in f:
                ret=line.split()
                if ret[0] == "btime":
                    btime=ret[1]
        if btime:
            return time.strftime("%Y-%m-%d %H:%M:%s",time.localtime(float(btime)))
        else:
            return "0-0-0 00:00:00"
    def do_check_localtime(self):
        return int(time.time())