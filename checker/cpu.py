#!/usr/bin/env python
# -*- coding:utf8 -*-
#abc
__author__='haibo.zhang'

from . import CheckerBase
import time
import os

class Checker(CheckerBase):
    def __init__(self,filepath="/proc/stat"):
        super(Checker,self).__init__()
        self.stat_path=filepath
        self.cpucount=0
        self._old_data={}
        self.interval=10
    def _get_raw_data(self):
        kvps={}
        fh=open(self.stat_path,"r")
        keylines=fh.readlines()
        fh.close()
        for line in keylines:
            kv_list=line.split()
            kvps.update({kv_list[0]:kv_list[1:]})
        return kvps
    def _get_cpucount(self):
        kvps={}
        fh=open(self.stat_path,"r")
        keylines=fh.readlines()
        fh.close()
        for line in keylines:
            kv_list=line.split()
            if kv_list[0][0:3] == "cpu":
                self.cpucount+=1
        return self.cpucount-1

    def _update_old_data(self,key,value):
        self._old_data.update({key:value})
            
    def do_check_cputime(self):
        current_raw_data = self._get_raw_data()
        cputime = 0
        for i in current_raw_data["cpu"]:
            cputime +=long(i)
        if "cputime" in self._old_data.keys():
            o_cputime = self._old_data["cputime"]
            self._update_old_data("cputime", cputime)
            return int((long(cputime) - long(o_cputime))/100)
        else:
            self._update_old_data("cputime", cputime)
            return 0
    
    def do_check_idle(self):
        current_raw_data = self._get_raw_data()
        idle = current_raw_data["cpu"][3]
        if "idle" in self._old_data.keys():
            o_idle = self._old_data["idle"]
            self._update_old_data("idle", idle)
            return int((long(idle) - long(o_idle))/100)
        else:
            self._update_old_data("idle", idle)
            return 0
    def do_check_systime(self):
        current_raw_data = self._get_raw_data()
        systime = current_raw_data["cpu"][2]
        if "systime" in self._old_data.keys():
            o_systime = self._old_data["systime"]
            self._update_old_data("systime", systime)
            return int((long(systime) - long(o_systime))/100)
        else:
            self._update_old_data("systime", systime)
            return 0
    def do_check_usertime(self):
        current_raw_data = self._get_raw_data()
        usertime = current_raw_data["cpu"][0]
        if "usertime" in self._old_data.keys():
            o_usertime = self._old_data["usertime"]
            self._update_old_data("usertime", usertime)
            return int((long(usertime) - long(o_usertime))/100)
        else:
            self._update_old_data("usertime", usertime)
            return 0
    
    def do_check_iowait(self):
        current_raw_data = self._get_raw_data()
        iowait = current_raw_data["cpu"][4]
        if "iowait" in self._old_data.keys():
            o_iowait = self._old_data["iowait"]
            self._old_data["iowait"] = iowait
            return int((long(iowait) - long(o_iowait))/100)
        else:
            self._update_old_data("iowait", iowait)
            return 0

    def do_check_hard_interrupt(self):
        current_raw_data = self._get_raw_data()
        irq = current_raw_data["cpu"][5]
        if "irq" in self._old_data.keys():
            o_irq = self._old_data["irq"]
            self._update_old_data("irq", irq)
            return int((long(irq) - long(o_irq))/100)
        else:
            self._update_old_data("irq", irq)
            return 0

    def do_check_soft_interrupt(self):
        current_raw_data = self._get_raw_data()
        softirq = current_raw_data["cpu"][6]
        if "softirq" in self._old_data.keys():
            o_softirq = self._old_data["softirq"]
            self._update_old_data("softirq", softirq)    
            return int((long(softirq) - long(o_softirq))/100)
        else:
            self._update_old_data("softirq", softirq)
            return 0

    def do_check_cpu_usage(self):
        current_raw_data = self._get_raw_data()
        cputime = 0
        for time in current_raw_data["cpu"]:
            cputime += long(time)
        idle = current_raw_data["cpu"][3]
        if "cputime_idle" in self._old_data.keys():
            o_cputime = self._old_data["cputime_idle"]["cputime"]
            o_idle = self._old_data["cputime_idle"]["idle"]
            cputime_idle={};
            cputime_idle.update({"cputime":cputime})
            cputime_idle.update({"idle":idle})
            self._update_old_data("cputime_idle", cputime_idle)
            value = ((((long(cputime) - long(idle))) - (long(o_cputime) - long(o_idle)))/float(long(cputime) - long(o_cputime)))*100
            value = str("%.2f"%value)
            return value
        else:
            cputime_idle={}
            cputime_idle.update({"cputime":cputime})
            cputime_idle.update({"idle":idle})
            self._update_old_data("cputime_idle", cputime_idle)
            return 0

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a","--argument",dest="arg")
    options,agrs = parser.parse_args()
    cpu=CPU("/proc/stat")
    print cpu.do_check_iowait()
        
    
