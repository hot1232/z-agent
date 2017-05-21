#!/usr/bin/python2.7
# -*- coding:utf8 -*-
#__author__='kai.xu'

from . import CheckerBase
from lib.decorator import time_me



class Checker(CheckerBase):
    def _init(self,filepath="/proc/meminfo"):
        self.mem_path=filepath
        self.interval=60
    def _get_all_data(self):
        lins_mem=open(self.mem_path,"r").readlines()
        keys=[]
        value=[]
        for i in range(0,len(lins_mem)):
            keys.append(lins_mem[i].split()[0][0:-1])
            value.append(lins_mem[i].split()[1])
        self.data=dict(map(None,keys,value))
        return self.data
    #@time_me
    def _do_check_common(self,same_key):
        now_important_data = self._get_all_data()
        ret = now_important_data.get(same_key,0)
        return int(ret)*1024
    #@time_me
    def do_check_MemTotal(self):
        return self._do_check_common('MemTotal')
    
    #@time_me
    def do_check_MemFree(self):
        return self._do_check_common('MemFree')
    
    def do_check_MemFree_percent(self):
        return "%0.2f"%(self.do_check_MemFree()/float(self.do_check_MemTotal()))
    
    #@time_me
    def do_check_Buffers(self):
        return self._do_check_common('Buffers')
    
    #@time_me
    def do_check_Cached(self):
        return self._do_check_common('Cached')
    
    #@time_me
    def do_check_SwapCached(self):
        return self._do_check_common('SwapCached')
    
    #@time_me
    def do_check_SwapTotal(self):
        return self._do_check_common('SwapTotal')
    
    #@time_me
    def do_check_SwapFree(self):
        return self._do_check_common('SwapFree')
    
    #@time_me
    def do_check_Dirty(self):
        return self._do_check_common('Dirty')
    
    #@time_me
    def do_check_Writeback(self):
        return self._do_check_common('Writeback')
    
    #@time_me
    #def do_check_AnonPages(self):
        #return self._do_check_common('AnonPages')
    
    #@time_me
    #def do_check_Mapped(self):
        #return self._do_check_common('Mapped')
    
    #@time_me
    #def do_check_Slab(self):
        #return self._do_check_common('Slab')
    
    #@time_me
    #def do_check_Active(self):
        #return self._do_check_common('Active')
    
    #@time_me
    #def do_check_Inactive(self):
        #return self._do_check_common('Inactive')
    
    #@time_me
    #def do_check_VmallocTotal(self):
        #return self._do_check_common('VmallocTotal')
    
    #@time_me
    #def do_check_VmallocUsed(self):
        #return self._do_check_common('VmallocUsed')

if __name__ == "__main__":
    pass
