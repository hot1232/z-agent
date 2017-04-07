#!/usr/bin/env python
# -*- coding:utf8 -*-

import gevent
import time
import traceback

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)

from abc import abstractmethod

from lib.link import Chanels
from lib.log import logging

class DiscoveryBase(gevent.Greenlet):
    def __new__(cls, *args, **kw):      
        if not hasattr(cls, '_instance'):
            cls._instance={}
            orig = super(DiscoveryBase, cls)
            cls._instance[key]=orig.__new__(cls, *args, **kw)
        return cls._instance
            
    def __init__(self,interval=None,run=None,timeout=None,*args, **kwargs):
        super(DiscoveryBase,self).__init__(run=run,*args,**kwargs)
        if interval:
            self.interval=interval
        else:
            self.interval=60
        if not timeout is None:
            self.timeout=gevent.Timeout(timeout)
        else:
            self.timeout=gevent.Timeout(3)
        self.chanel=Chanels()
        if not self.chanel["discovery"]:
            self.chanel.append("discovery")
        if not self.chanel["discovery-sender"]:
            self.chanel.append("discovery-sender")        
        self.logger=logging.getLogger(__name__)
        self.logger.info("Discoverier: %s 's interval is: %s"%(__name__,self.interval))
        self.data=None
        self._init(*args,**kwargs)
    @abstractmethod
    def _init(self,*args,**kwargs):
        pass
    
    @abstractmethod
    def run(self,**kwargs):
        pass
    
    def notify_monitor(self):
        pass
    
    def build_discovery_data(self):
        pass