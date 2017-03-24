#!/usr/bin/env python
# -*- coding:utf8 -*-

from . import CheckerBase
import os
import time
import unittest
import copy

#import gc

#gc.set_threshold(0) #turn off gc

class Checker(CheckerBase):
    def _init(self):
        self._netstat_fp=open("/proc/net/netstat")
        self._netsnmp_fp=open("/proc/net/snmp")
        self_old_data={}
        self_cur_data={}
        self._checktime=0
        self.interval=10
    
    def __getattr__(self,key):
        if key.startswith("do_check_"):
            return self._get_key(key.replace("do_check_",""))
        else:
            pass
            #return self._get_key(key)
    
    def _array_to_dict(self,key,value):
        return dict([(key,value)])
    
    def _get_raw_data(self):
        kvps={}
        if int(time.time()) - self._checktime >= self.interval:
            self._netsnmp_fp.seek(0)
            self._netstat_fp.seek(0)
            lines_netsnmp=self._netstat_fp.readlines()
            data={}
            for i in range(0,len(lines_netsnmp),2):
                keys=lines_netsnmp[i].split()[1:]
                values=[long(v)for v in lines_netsnmp[i+1].split()[1:]]
                data.update(dict(map(None,keys,values)))
            
            lines_netstat=self._netstat_fp.readlines()
            for i in range(0,len(lines_netstat),2):
                keys=lines_netstat[i].split()[1:]
                values=[long(v) for v in lines_netstat[i+1].split()[1:]]
                data.update(dict(map(None,keys,values)))

            if not self._cur_data:
                self._old_data=copy.deepcopy(data)
                for k in self._old_data:
                    self._old_data[k]=0                
            else:
                self._old_data=copy.deepcopy(self._cur_data)
            self._cur_data=copy.deepcopy(data)
            
            self._checktime=int(time.time())    
    
    def _get_key(self,key):
        self._get_raw_data()
        return int(self._cur_data[key]-self._old_data[key])
    
    def __dir__(self):
        self._get_raw_data()
        t=["do_check_%s"%k for k in self._cur_data]
        return t

class TestNetstat(unittest.TestCase):
    def test_get_all_key(self):
        s=Netstat()
        print(s.keys())
    
    def test_get_all(self):
        s=Netstat()
        for i in s.keys():
            print("%s: %s"%(i,getattr(s,i)))   
            

if __name__ == "__main__":
    pass