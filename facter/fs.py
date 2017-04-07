#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
from . import FacterBase

class Facter(FacterBase):
    def _init(self):
        with open("/etc/mtab","r") as f:
            self.partitions=[line.split()[1] for line in f if line.split()[2] in ["xfs","ext4","ext3"]]
    
    def facter_partition_count(self):
        return len(self.partitions)
    
    def facter_partition_total_size(self):
        data=[]
        for part in self.partitions:
            temp=os.statvfs("part")
            data.append({part:temp.f_bsize*f_blocks/3072})
        return data