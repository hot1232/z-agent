#!/usr/bin/env python
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()

from facter.hostname import Facter
from lib.log import logging
from lib import protobix

from . import SenderBase


class Sender(SenderBase): 
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
            self.logger.exception("send zbx data to : %s failed"%self.config.get("zabbix-server").get("host"))