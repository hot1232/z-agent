#!/usr/bin/env python
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()
import protobix


class Sender(object):   
    def __init__(self,mType="items"):
        self._name="zbx"
        self.data=protobix.DataContainer(mType, "172.16.5.38", 10051)
        self.hostname="t2"
    def add(self,data):
        self.data.add({self.hostname:data})
    def send(self):
        try:
            ret = self.data.send(self.data)
            if not ret:
                print "Ooops. Something went wrong when sending data to Zabbix"
        except Exception,e:
            import traceback
            traceback.print_exc()
            print("send error: %s"%e)