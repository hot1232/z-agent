#!/usr/bin/env python
# -*- coding:utf8 -*-
#abc
__author__='haibo.zhang'

from . import CheckerBase
from lib.decorator import time_me
import time
import os
import copy

class Checker(CheckerBase):
    def _init(self,stat="/proc/stat",load="/proc/loadavg"):
        self.stat_path=stat
        self.load_path=load
        self.cpucount=0
        self._old_data={}
        self.interval=10
        self._checkcputime=0
        self._checkloadtime=0
        self._cur_raw_data={}
        self._cur_load_data=[]
    def _get_raw_data(self):
        kvps={}
        if int(time.time()) - self._checkcputime >= self.interval:
            with open(self.stat_path,"r") as fh:
                for line in fh:
                    kv_list=line.split()
                    kvps.update({kv_list[0]:[long(v) for v in kv_list[1:]]})
            if not self._cur_raw_data:
                self._old_data=copy.deepcopy(kvps)
                for k in self._old_data:
                    self._old_data[k]=[0 for i in self._old_data[k]]                
            else:
                self._old_data=copy.deepcopy(self._cur_raw_data)
            self._cur_raw_data=copy.deepcopy(kvps)
            self._checkcputime=int(time.time())
        return self._cur_raw_data
    def _get_loadavg(self):
        if int(time.time()) - self._checkloadtime >= self.interval:
            with open(self.load_path, "r") as load_handle:
                self._cur_load_data = [la for la in load_handle.readline().split()[0:3]]
            self._checkloadtime=int(time.time())

    def _get_cpucount(self):
        self.fh.seek(0)
        keylines=self.fh.readlines()
        for line in keylines:
            kv_list=line.split()
            if kv_list[0][0:3] == "cpu":
                self.cpucount+=1
        self.fh.seek(0)
        return self.cpucount-1
            
#    def _get_cputime(self):
#        current_raw_data = self._get_raw_data()
#        cputime = sum(long(i) for i in current_raw_data["cpu"])
#        value=0
#        if "cputime" in self._old_data.keys():
#            o_cputime = self._old_data["cputime"]
#            value=int(cputime - o_cputime)
#        self._update_old_data("cputime", cputime)
#        return value
    def do_check_loadavg_1(self):
        self._get_loadavg()
        return self._cur_load_data[0]
    def do_check_loadavg_5(self):
        self._get_loadavg()
        return self._cur_load_data[1]
    def do_check_loadavg_15(self):
        self._get_loadavg()
        return self._cur_load_data[2]
    #@time_me
    def do_check_idle(self):
        self._get_raw_data()
        idle = self._cur_raw_data["cpu"][3]
        o_idle=self._old_data["cpu"][3]
        o_cputime = sum(long(i)for i in self._old_data["cpu"])
        cputime=sum(long(i)for i in self._cur_raw_data["cpu"])
        return "%.2f"%((idle-o_idle)/float(cputime-o_cputime)*100)

    def do_check_systime(self):
        self._get_raw_data()
        cputime =sum([long(v) for v in self._cur_raw_data["cpu"]])
        o_cputime =sum([long(v) for v in self._old_data["cpu"]])         
        systime = self._cur_raw_data["cpu"][2]
        o_systime = self._old_data["cpu"][2]
        return "%.2f"%((systime - o_systime)/(cputime - o_cputime)*100)

    def do_check_usertime(self):
        self._get_raw_data()
        cputime =sum([long(v) for v in self._cur_raw_data["cpu"]])
        o_cputime =sum([long(v) for v in self._old_data["cpu"]])         
        usertime = self._cur_raw_data["cpu"][0]
        o_usertime = self._old_data["cpu"][0]
        return "%.2f"%((usertime-o_usertime)/float(cputime-o_cputime)*100)
    
    def do_check_iowait(self):
        self._get_raw_data()
        cputime =sum([long(v) for v in self._cur_raw_data["cpu"]])
        o_cputime =sum([long(v) for v in self._old_data["cpu"]])        
        iowait = self._cur_raw_data["cpu"][4]
        o_iowait=self._old_data["cpu"][4]
        return "%.2f"%((iowait-o_iowait)/float(cputime-o_cputime)*100)

    def do_check_ctxt(self):
        self._get_raw_data()
        ctxt = self._cur_raw_data["ctxt"][0]
        o_ctxt=self._old_data["ctxt"][0]
        return int(ctxt-o_ctxt)

    def do_check_hard_interrupt(self):
        self._get_raw_data()
        irq = self._cur_raw_data["cpu"][5]
        o_irq = self._old_data["cpu"][5]
        return int(irq-o_irq)

    def do_check_soft_interrupt(self):
        self._get_raw_data()
        softirq = self._cur_raw_data["cpu"][6]
        o_softirq = self._old_data["cpu"][6]
        return int(softirq-o_softirq)

    def do_check_cpu_usage(self):
        self._get_raw_data()
        cputime =sum([long(v) for v in self._cur_raw_data["cpu"]])
        o_cputime =sum([long(v) for v in self._old_data["cpu"]])
        idle = self._cur_raw_data["cpu"][3]
        o_idle = self._old_data["cpu"][3]
        cputime=cputime-o_cputime
        usage=cputime-idle+o_idle
        return "%.2f"%(usage/float(cputime)*100)

if __name__ == "__main__":
    pass
        
    
