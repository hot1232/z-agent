#!/usr/bin/env python2.7
# -*- coding:utf8 -*

from . import CheckerBase
import os
import time

class Checker(CheckerBase):
    mode="auto"
    def _init(self,*args,**kwargs):
        if self._name:
            self.suffix="[%s]"%self._name
            self.stat_path = "/proc/diskstats"
            self._old_data = (0,0,0,0)
            self.partitions = {}
            self._io_ret = []
            self._checktime = 0
            with open("/etc/mtab","r") as f:
                self.partitions = [line.split()[0] for line in f if line.split()[2] in ["xfs", "ext4", "ext3"] and line.split()[1] == self._name ]
            if os.path.islink(self.partitions[0]):
                self.partitions=os.path.realpath(self.partitions[0]).split("/")[-1]
            else:
                self.partitions=self.partitions[0].split("/")[-1]

    def _get_raw_data(self):
        if int(time.time()) - self._checktime >= self.interval:
            with open(self.stat_path,"r") as fp:
                for line in fp:
                    line_arr=line.split()
                    if line_arr[2] == self.partitions:
                        cur_data = (long(line_arr[3]),long(line_arr[6]),long(line_arr[7]),long(line_arr[10]))
            self._io_ret=map(lambda x,y:x-y,cur_data,self._old_data)
            self._old_data = cur_data
            self._checktime = int(time.time())
        return self._io_ret
    
    def do_check_free_size(self):
        c=os.statvfs(self._name)
        return "%0.2f"%(c.f_bfree/float(c.f_blocks)*100)
    
    def do_check_free_inode(self):
        c=os.statvfs(self._name)
        return '%0.2f'%float(c.f_ffree/float(c.f_files)*100)
    
    def do_check_total_size(self):
        c=os.statvfs(self._name)
        return c.f_blocks*c.f_bsize
    
    def do_check_time_per_write(self):
        data = self._get_raw_data()
        if data[2] == 0:
            ret = "0.000"
        else:
            ret = "%0.3f"%(data[3]/float(data[2]))
        return ret
    
    def do_check_time_per_read(self):
        data = self._get_raw_data()
        if data[0] == 0:
            ret = "0.000"
        else:
            ret = "%0.3f"%(data[1]/float(data[0]))
        return ret
    
    def do_check_vdisk_read(self):
        data = self._get_raw_data()
        return data[0]
    
    def do_check_vdisk_write(self):
        data = self._get_raw_data()
        return data[3]    
