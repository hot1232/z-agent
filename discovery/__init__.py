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
        self._init(*args,**kwargs)
    @abstractmethod
    def _init(self,*args,**kwargs):
        pass    