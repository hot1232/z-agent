#!/usr/bin/env python
# -*- coding:utf8 -*

from . import CheckerBase
import os

class Checker(CheckerBase):
    mode="auto"
    def _init(self,*args,**kwargs):
        if self._name:
            self.suffix=":%s"%self._name

    def do_check_free_size(self):
        c=os.statvfs(self._name)
        return "%0.2f"%(c.f_blocks/float(c.f_bfree))
    
    def do_check_free_inode(self):
        c=os.statvfs(self._name)
        return "%0.2f"%(c.f_ffree/float(c.f_files))
    
    def do_check_total_size(self):
        c=os.statvfs(self._name)
        return c.f_blocks*c.f_bsize/1024/1024