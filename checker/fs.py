#!/usr/bin/env python
# -*- coding:utf8 -*

from . import CheckerBase
import os

class Checker(CheckerBase):
    mode="auto"
    def do_check_free_size(self):
        c=os.statvfs(self._name)
        return "%0.2f"%(c.blocks/float(c.bfree))
    
    def do_check_free_inode(self):
        c=os.statvfs(self._name)
        return "%0.2f"%(c.ffree/float(c.files))
    
    def do_check_total_size(self):
        c=os.statvfs(self._name)
        return c.blocks*c.f_bsize/1024/1024