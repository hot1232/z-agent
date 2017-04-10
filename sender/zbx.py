#!/usr/bin/env python
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()

from facter.hostname import Facter
from lib.log import logging
from lib import protobix

from . import SenderBase


class Sender(SenderBase):
    def __new__(cls, *args, **kw):       
        if not hasattr(cls, '_instance'):
            cls._instance={}
            orig = super(FacterBase, cls)
            cls._instance=orig.__new__(cls, *args, **kw)
        return cls._instance    
    def _init(self,mType="items"):
        self._name="zbx"
        self.data=protobix.DataContainer(mType, self.config.get("zabbix-server").get("host"), 10051)
        self.hostname=Facter()["fqdn"]
        self.logger=logging.getLogger(self.__module__)
    def add(self,data):
        self.logger.debug("add data: %s"%data)
        self.data.add({self.hostname:data})
    def send(self):
        try:
            ret = self.data.send(self.data)
            if not ret:
                self.logger.warn("zbx response None")
        except Exception,e:
            self.logger.exception(e)