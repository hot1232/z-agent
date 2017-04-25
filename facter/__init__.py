#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import gc
from abc import abstractmethod
LIBPATH = os.path.dirname(__file__).rstrip(__name__)
if not LIBPATH in os.sys.path:
    os.sys.path.append(LIBPATH)
    
import time
    
import gevent
from lib.log import logging

class FacterBase(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(FacterBase, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__module__)
        super(FacterBase,self).__init__(run=None,*args,**kwargs)
        self._init(*args, **kwargs)

    @abstractmethod
    def _init(self, *args, **kwargs):
        pass

    def __getitem__(self, key):
        tgt = getattr(self, "facter_%s"%key)
        if callable(tgt):
            return tgt()
        else:
            return tgt

    def __iter__(self):
        return iter([x.replace("facter_", "") for x in dir(self) if x.startswith("facter_")])
    