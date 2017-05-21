#!/usr/bin/env python2.7
# -*- coding:utf8 -*-
import os
from . import FacterBase

class Facter(FacterBase):
    def _init(self):
        with open("/etc/mtab", "r") as f:
            self.partitions = [line.split()[1] for line in f if line.split()[2] in ["xfs", "ext4", "ext3"]]

    def facter_partition_count(self):
        return len(self.partitions)

    def facter_partition_total_size(self):
        data = {}
        for part in self.partitions:
            temp = os.statvfs(part)
            data.update({part:temp.f_bsize*temp.f_blocks/1048576})
        return data
    