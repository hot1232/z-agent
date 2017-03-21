#!/usr/bin/python
# -*- coding:utf8 -*-
#__author__='kai.xu'

from . import CheckerBase
import os
import time
import re
import sys
import json



class Checker(CheckerBase):
    def _init(self,filepath="/proc/meminfo"):
        self.mem_path=filepath
        self.old_data={}
        self.interval=180
    def _get_all_data(self):
        lins_mem=open(self.mem_path,"r").readlines()
        keys=[]
        value=[]
        for i in range(0,len(lins_mem)):
            keys.append(lins_mem[i].split()[0][0:-1])
            value.append(lins_mem[i].split()[1])
        data=dict(map(None,keys,value))
        return data
    def _update_data_for_old(self,keys,value):
        self.old_data.update({keys:value})
    def _do_check_common(self,same_key):
        now_important_data = self._get_all_data()
        memfree = now_important_data[same_key]
        if same_key in self.old_data.keys():
            old_memfree = self.old_data[same_key]
            self._update_data_for_old(same_key, memfree)
            return int(memfree - old_memfree)
        else:
            self._update_data_for_old(same_key, memfree)
            return 0
    def do_check_MemTotal(self):
        self._do_check_common('MemTotal')
    def do_check_MemFree(self):
        self._do_check_common('MemFree')
    def do_check_Buffers(self):
        self._do_check_common('Buffers')
    def do_check_Cached(self):
        self._do_check_common('Cached')
    def do_check_SwapCached(self):
        self._do_check_common('SwapCached')
    def do_check_SwapTotal(self):
        self._do_check_common('SwapTotal')
    def do_check_SwapFree(self):
        self._do_check_common('SwapFree')
    def do_check_Dirty(self):
        self._do_check_common('Dirty')
    def do_check_Writeback(self):
        self._do_check_common('Writeback')
    def do_check_AnonPages(self):
        self._do_check_common('AnonPages')
    def do_check_Mapped(self):
        self._do_check_common('Mapped')
    def do_check_Slab(self):
        self._do_check_common('Slab')
    def do_check_Active(self):
        self._do_check_common('Active')
    def do_check_Inactive(self):
        self._do_check_common('Inactive')
    def do_check_VmallocTotal(self):
        self._do_check_common('VmallocTotal')
    def do_check_VmallocUsed(self):
        self._do_check_common('VmallocUsed')

if __name__ == "__main__":
    pass
