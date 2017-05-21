#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

import struct
from lib.log import logging
import json
from lib import protobix
from . import SenderBase
from facter.hostname import Facter

class Sender(SenderBase): 
    def _init(self,mType="lld"):
        self._name="zbx"
        self.data=protobix.DataContainer(mType, self.config.get("zabbix-server").get("host"), 10051)
        self.hostname=Facter()["hostname"]
        self.logger=logging.getLogger(self.__module__)
    def add(self,key,data):
        self.logger.debug("add data: %s"%data)
        self.data.add_item(self.hostname,key,data)
    def send(self):
        try:
            self.logger.debug("send discovery data: %s"%self.data)
            ret = self.data.send(self.data)
            if not ret:
                self.logger.warn("zbx response None")
        except Exception,e:
            self.logger.exception("send zbx data to : %s failed"%self.config.get("zabbix-server").get("host"))