#!/usr/bin/env python
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()
import protobix


class Sender(object):   
    def __init__(self,mType="items"):
        self._name="zbx"
        self.data=protobix.DataContainer(mType, "172.16.5.220", 10051)
        self.hostname="localhost"
    
    def send(self,data):
        try:
            data={self.hostname:data}
            self.data.add(data)
            print("send data: %s"%data)
            ret = self.data.send(self.data)
            if not ret:
                print "Ooops. Something went wrong when sending data to Zabbix"    
            print "Everything is OK"
        except Exception,e:
            print("send error: %s"%e)