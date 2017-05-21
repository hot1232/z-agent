#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()

from facter.hostname import Facter
from lib.log import logging
from lib import protobix

from . import SenderBase
from lib.decorator import time_me


class Sender(SenderBase): 
    def _init(self,mType="items"):
        self.data=protobix.DataContainer(mType, self.config.get("zabbix-server").get("host"), 10051)
        self.hostname=Facter()["hostname"]       
    def add(self,key=None,value=None,clock=None):
        self.logger.debug("add data: %s : %s at %s",key,value,clock)
        self.data.add_item(self.hostname,key,value,clock)
    
    #@time_me
    def send(self):
        try:
            ret = self.data.send(self.data)
            if not ret:
                self.logger.warn("zbx response None")
            else:
                self.logger.debug("send data success")
        except Exception,e:
            self.logger.exception("send zbx data to : %s failed"%self.config.get("zabbix-server").get("host"))
