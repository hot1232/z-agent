#!/usr/bin/env python
# -*- coding:utf8 -*

from . import CheckerBase
import os
import time
import psutil
from facter.interface import Facter

class Checker(CheckerBase):
    mode="auto"
    def _init(self,*args,**kwargs):
        if self._name:
            self.suffix="[%s]"%self._name
            self._old_data = {}
            self._io_ret = {}
            self._checktime = 0
            for intf in Facter().facter_interfaces:
                if not self._old_data.has_key(intf):
                    self._old_data.update({intf:{"bytes_sent":0,"bytes_recv":0}})

    def _get_raw_data(self):
        if int(time.time()) - self._checktime >= self.interval:
            cur_data={}
            data=psutil.net_io_counters(pernic=True)
            for intf in Facter().facter_interfaces:
                cur_data.update({intf:{"bytes_sent":data.get(intf).bytes_sent,"bytes_recv":data.get(intf).bytes_recv}})
                self._io_ret.update({intf:{"bytes_sent":cur_data[intf]["bytes_sent"]-self._old_data[intf]["bytes_sent"],"bytes_recv":cur_data[intf]["bytes_recv"]-self._old_data[intf]["bytes_recv"]}})
            self._old_data = cur_data
            self._checktime = int(time.time())
        return self._io_ret
    
    def do_check_sent(self):
        data=self._get_raw_data()
        return data.get(self._name).get("bytes_sent")/1024
    
    def do_check_recv(self):
        data=self._get_raw_data()
        return data.get(self._name).get("bytes_recv")/1024