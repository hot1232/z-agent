#!/usr/bin/env python
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()

from facter.hostname import Facter
from lib.log import logging
from lib import protobix


class Sender(object):   
    def __init__(self,mType="items"):
        self._name="zbx"
        self.data=protobix.DataContainer(mType, "172.16.5.38", 10051)
        self.hostname=Facter()["fqdn"]
        self.logger=logging.getLogger(__name__)
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